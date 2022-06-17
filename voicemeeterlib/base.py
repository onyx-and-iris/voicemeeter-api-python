import ctypes as ct
import time
from abc import abstractmethod
from functools import partial
from threading import Thread
from typing import Iterable, NoReturn, Optional, Self, Union

from .cbindings import CBindings
from .error import VMError
from .kinds import KindId
from .subject import Subject
from .util import polling, script


class Remote(CBindings):
    """Base class responsible for wrapping the C Remote API"""

    DELAY = 0.001

    def __init__(self, **kwargs):
        self.cache = {}
        self.subject = Subject()
        self._strip_levels, self._bus_levels = self.all_levels

        for attr, val in kwargs.items():
            setattr(self, attr, val)

    def __enter__(self) -> Self:
        """setup procedures"""
        self.login()
        self.init_thread()
        return self

    @abstractmethod
    def __str__(self):
        """Ensure subclasses override str magic method"""
        pass

    def init_thread(self):
        """Starts updates thread."""
        self.running = True
        t = Thread(target=self._updates, daemon=True)
        t.start()

    def _updates(self):
        """Continously update observers of dirty states."""
        while self.running:
            if self.pdirty:
                self.subject.notify("pdirty")
            if self.ldirty:
                self._strip_levels = self.strip_buf
                self._bus_levels = self.bus_buf
                self.subject.notify(
                    "ldirty",
                    (
                        self._strip_levels,
                        self._strip_comp,
                        self._bus_levels,
                        self._bus_comp,
                    ),
                )
            time.sleep(self.ratelimit)

    def login(self) -> NoReturn:
        """Login to the API, initialize dirty parameters"""
        res = self.vm_login()
        if res == 0:
            print(f"Successfully logged into {self}")
        elif res == 1:
            self.run_voicemeeter(self.kind.name)
        self.clear_dirty()

    def run_voicemeeter(self, kind_id: str) -> NoReturn:
        if kind_id not in (kind.name.lower() for kind in KindId):
            raise VMError(f"Unexpected Voicemeeter type: '{kind_id}'")
        if kind_id == "potato" and ct.sizeof(ct.c_voidp) == 8:
            value = KindId[kind_id.upper()].value + 3
        else:
            value = KindId[kind_id.upper()].value
        self.vm_runvm(value)
        time.sleep(1)

    @property
    def type(self) -> str:
        """Returns the type of Voicemeeter installation (basic, banana, potato)."""
        type_ = ct.c_long()
        self.vm_get_type(ct.byref(type_))
        return KindId(type_.value).name.lower()

    @property
    def version(self) -> str:
        """Returns Voicemeeter's version as a string"""
        ver = ct.c_long()
        self.vm_get_version(ct.byref(ver))
        v1 = (ver.value & 0xFF000000) >> 24
        v2 = (ver.value & 0x00FF0000) >> 16
        v3 = (ver.value & 0x0000FF00) >> 8
        v4 = ver.value & 0x000000FF
        return f"{v1}.{v2}.{v3}.{v4}"

    @property
    def pdirty(self) -> bool:
        """True iff UI parameters have been updated."""
        return self.vm_pdirty() == 1

    @property
    def mdirty(self) -> bool:
        """True iff MB parameters have been updated."""
        return self.vm_mdirty() == 1

    @property
    def ldirty(self) -> bool:
        """True iff levels have been updated."""
        self.strip_buf, self.bus_buf = self.all_levels
        self._strip_comp, self._bus_comp = (
            tuple(not a == b for a, b in zip(self.strip_buf, self._strip_levels)),
            tuple(not a == b for a, b in zip(self.bus_buf, self._bus_levels)),
        )
        return any(
            any(l)
            for l in (
                self._strip_comp,
                self._bus_comp,
            )
        )

    def clear_dirty(self):
        while self.pdirty or self.mdirty:
            pass

    @polling
    def get(self, param: str, is_string: Optional[bool] = False) -> Union[str, float]:
        """Gets a string or float parameter"""
        if is_string:
            buf = ct.create_unicode_buffer(512)
            self.call(
                partial(self.vm_get_parameter_string, param.encode(), ct.byref(buf))
            )
        else:
            buf = ct.c_float()
            self.call(
                partial(self.vm_get_parameter_float, param.encode(), ct.byref(buf))
            )
        return buf.value

    def set(self, param: str, val: Union[str, float]) -> NoReturn:
        """Sets a string or float parameter. Caches value"""
        if isinstance(val, str):
            if len(val) >= 512:
                raise VMError("String is too long")
            self.call(
                partial(self.vm_set_parameter_string, param.encode(), ct.c_wchar_p(val))
            )
        else:
            self.call(
                partial(
                    self.vm_set_parameter_float, param.encode(), ct.c_float(float(val))
                )
            )
        self.cache[param] = val

    @polling
    def get_buttonstatus(self, id: int, mode: int) -> int:
        """Gets a macrobutton parameter"""
        state = ct.c_float()
        self.call(
            partial(
                self.vm_get_buttonstatus,
                ct.c_long(id),
                ct.byref(state),
                ct.c_long(mode),
            )
        )
        return int(state.value)

    def set_buttonstatus(self, id: int, state: int, mode: int) -> NoReturn:
        """Sets a macrobutton parameter. Caches value"""
        c_state = ct.c_float(float(state))
        self.call(
            partial(self.vm_set_buttonstatus, ct.c_long(id), c_state, ct.c_long(mode))
        )
        self.cache[f"mb_{id}_{mode}"] = int(c_state.value)

    def get_num_devices(self, direction: str = None) -> int:
        """Retrieves number of physical devices connected"""
        if direction not in ("in", "out"):
            raise VMError("Expected a direction: in or out")
        func = getattr(self, f"vm_get_num_{direction}devices")
        return func()

    def get_device_description(self, index: int, direction: str = None) -> tuple:
        """Returns a tuple of device parameters"""
        if direction not in ("in", "out"):
            raise VMError("Expected a direction: in or out")
        type_ = ct.c_long()
        name = ct.create_unicode_buffer(256)
        hwid = ct.create_unicode_buffer(256)
        func = getattr(self, f"vm_get_desc_{direction}devices")
        func(
            ct.c_long(index),
            ct.byref(type_),
            ct.byref(name),
            ct.byref(hwid),
        )
        return (name.value, type_.value, hwid.value)

    @property
    def all_levels(self) -> Iterable:
        """
        returns both level arrays (strip_levels, bus_levels) BEFORE math conversion

        strip levels in PREFADER mode.
        """
        return (
            tuple(
                self.get_level(0, i)
                for i in range(2 * self.kind.phys_in + 8 * self.kind.virt_in)
            ),
            tuple(
                self.get_level(3, i)
                for i in range(8 * (self.kind.phys_out + self.kind.virt_out))
            ),
        )

    def get_level(self, type_: int, index: int) -> float:
        """Retrieves a single level value"""
        val = ct.c_float()
        self.vm_get_level(ct.c_long(type_), ct.c_long(index), ct.byref(val))
        return val.value

    @script
    def sendtext(self, script: str):
        """Sets many parameters from a script"""
        if len(script) > 48000:
            raise ValueError("Script too large, max size 48kB")
        self.call(partial(self.vm_set_parameter_multi, script.encode()))
        time.sleep(self.DELAY * 5)

    def apply(self, data: dict):
        """
        Sets all parameters of a dict

        minor delay between each recursion
        """

        def param(key):
            obj, m2, *rem = key.split("-")
            index = int(m2) if m2.isnumeric() else int(*rem)
            if obj in ("strip", "bus", "button"):
                return getattr(self, obj)[index]
            elif obj == "vban":
                return getattr(getattr(self, obj), f"{m2}stream")[index]
            else:
                raise ValueError(obj)

        [param(key).apply(datum).then_wait() for key, datum in data.items()]

    def apply_config(self, name):
        """applies a config from memory"""
        error_msg = (
            f"No config with name '{name}' is loaded into memory",
            f"Known configs: {list(self.configs.keys())}",
        )
        try:
            self.apply(self.configs[name])
            print(f"Profile '{name}' applied!")
        except KeyError as e:
            print(("\n").join(error_msg))

    def logout(self) -> NoReturn:
        """Wait for dirty parameters to clear, then logout of the API"""
        self.clear_dirty()
        time.sleep(0.1)
        res = self.vm_logout()
        if res == 0:
            print(f"Successfully logged out of {self}")

    def end_thread(self):
        self.running = False

    def __exit__(self, exc_type, exc_value, exc_traceback) -> NoReturn:
        """teardown procedures"""
        self.end_thread()
        self.logout()
