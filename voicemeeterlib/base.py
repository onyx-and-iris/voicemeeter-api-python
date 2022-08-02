import ctypes as ct
import time
from abc import abstractmethod
from functools import partial
from threading import Thread
from typing import Iterable, NoReturn, Optional, Self, Union

from .cbindings import CBindings
from .error import CAPIError, VMError
from .inst import bits
from .kinds import KindId
from .misc import Event, Midi
from .subject import Subject
from .util import comp, grouper, polling, script


class Remote(CBindings):
    """Base class responsible for wrapping the C Remote API"""

    DELAY = 0.001

    def __init__(self, **kwargs):
        self.strip_mode = 0
        self.cache = {}
        self.cache["strip_level"], self.cache["bus_level"] = self._get_levels()
        self.midi = Midi()
        self.subject = Subject()
        self.running = None

        for attr, val in kwargs.items():
            setattr(self, attr, val)

        self.event = Event(self.subs)

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
        print(f"Listening for {', '.join(self.event.get())} events")
        t = Thread(target=self._updates, daemon=True)
        t.start()

    def _updates(self):
        """
        Continously update observers of dirty states.

        Generate _strip_comp, _bus_comp and update level cache if ldirty.

        Runs updates at a rate of self.ratelimit.
        """
        while self.running:
            if self.event.pdirty and self.pdirty:
                self.subject.notify("pdirty")
            if self.event.mdirty and self.mdirty:
                self.subject.notify("mdirty")
            if self.event.midi and self.get_midi_message():
                self.subject.notify("midi")
            if self.event.ldirty and self.ldirty:
                self._strip_comp, self._bus_comp = (
                    tuple(
                        not x for x in comp(self.cache["strip_level"], self._strip_buf)
                    ),
                    tuple(not x for x in comp(self.cache["bus_level"], self._bus_buf)),
                )
                self.cache["strip_level"] = self._strip_buf
                self.cache["bus_level"] = self._bus_buf
                self.subject.notify("ldirty")

            time.sleep(self.ratelimit if self.event.any() else 0.5)

    def login(self) -> NoReturn:
        """Login to the API, initialize dirty parameters"""
        res = self.vm_login()
        if res == 1:
            self.run_voicemeeter(self.kind.name)
        elif res != 0:
            raise CAPIError(f"VBVMR_Login returned {res}")
        print(f"Successfully logged into {self}")
        self.clear_dirty()

    def run_voicemeeter(self, kind_id: str) -> NoReturn:
        if kind_id not in (kind.name.lower() for kind in KindId):
            raise VMError(f"Unexpected Voicemeeter type: '{kind_id}'")
        if kind_id == "potato" and bits == 8:
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
        return "{}.{}.{}.{}".format(
            (ver.value & 0xFF000000) >> 24,
            (ver.value & 0x00FF0000) >> 16,
            (ver.value & 0x0000FF00) >> 8,
            ver.value & 0x000000FF,
        )

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
        self._strip_buf, self._bus_buf = self._get_levels()
        return not (
            self.cache.get("strip_level") == self._strip_buf
            and self.cache.get("bus_level") == self._bus_buf
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

    def get_level(self, type_: int, index: int) -> float:
        """Retrieves a single level value"""
        val = ct.c_float()
        self.vm_get_level(ct.c_long(type_), ct.c_long(index), ct.byref(val))
        return val.value

    def _get_levels(self) -> Iterable:
        """
        returns both level arrays (strip_levels, bus_levels) BEFORE math conversion
        """
        return (
            tuple(
                self.get_level(self.strip_mode, i)
                for i in range(2 * self.kind.phys_in + 8 * self.kind.virt_in)
            ),
            tuple(
                self.get_level(3, i)
                for i in range(8 * (self.kind.phys_out + self.kind.virt_out))
            ),
        )

    def get_midi_message(self):
        n = ct.c_long(1024)
        buf = ct.create_string_buffer(1024)
        res = self.vm_get_midi_message(ct.byref(buf), n)
        if res > 0:
            vals = tuple(grouper(3, (int.from_bytes(buf[i]) for i in range(res))))
            for msg in vals:
                ch, pitch, vel = msg
                if not self.midi._channel or self.midi._channel != ch:
                    self.midi._channel = ch
                self.midi._most_recent = pitch
                self.midi._set(pitch, vel)
            return True
        elif res == -1 or res == -2:
            raise CAPIError(f"VBVMR_GetMidiMessage returned {res}")

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
        if res != 0:
            raise CAPIError(f"VBVMR_Logout returned {res}")
        print(f"Successfully logged out of {self}")

    def end_thread(self):
        self.running = False

    def __exit__(self, exc_type, exc_value, exc_traceback) -> NoReturn:
        """teardown procedures"""
        self.end_thread()
        self.logout()
