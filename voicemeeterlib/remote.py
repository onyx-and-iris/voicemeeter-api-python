import ctypes as ct
import logging
import time
from abc import abstractmethod
from queue import Queue
from typing import Iterable, NoReturn, Optional, Union

from .cbindings import CBindings
from .error import CAPIError, VMError
from .event import Event
from .inst import bits
from .kinds import KindId
from .misc import Midi, VmGui
from .subject import Subject
from .updater import Producer, Updater
from .util import grouper, polling, script

logger = logging.getLogger(__name__)


class Remote(CBindings):
    """Base class responsible for wrapping the C Remote API"""

    DELAY = 0.001

    def __init__(self, **kwargs):
        self.strip_mode = 0
        self.cache = {}
        self.midi = Midi()
        self.subject = self.observer = Subject()
        self.running = False
        self.event = Event(
            {k: kwargs.pop(k) for k in ("pdirty", "mdirty", "midi", "ldirty")}
        )
        self.gui = VmGui()
        self.logger = logger.getChild(self.__class__.__name__)

        for attr, val in kwargs.items():
            setattr(self, attr, val)

    def __enter__(self):
        """setup procedures"""
        self.login()
        if self.event.any():
            self.init_thread()
        return self

    @abstractmethod
    def __str__(self):
        """Ensure subclasses override str magic method"""
        pass

    def init_thread(self):
        """Starts updates thread."""
        self.running = True
        self.event.info()

        self.logger.debug("initiating events thread")
        queue = Queue()
        self.updater = Updater(self, queue)
        self.updater.start()
        self.producer = Producer(self, queue)
        self.producer.start()

    def login(self) -> NoReturn:
        """Login to the API, initialize dirty parameters"""
        self.gui.launched = self.call(self.vm_login, ok=(0, 1)) == 0
        if not self.gui.launched:
            self.logger.info(
                "Voicemeeter engine running but GUI not launched. Launching the GUI now."
            )
            self.run_voicemeeter(self.kind.name)
        self.logger.info(
            f"{type(self).__name__}: Successfully logged into {self} version {self.version}"
        )
        self.clear_dirty()

    def run_voicemeeter(self, kind_id: str) -> NoReturn:
        if kind_id not in (kind.name.lower() for kind in KindId):
            raise VMError(f"Unexpected Voicemeeter type: '{kind_id}'")
        if kind_id == "potato" and bits == 8:
            value = KindId[kind_id.upper()].value + 3
        else:
            value = KindId[kind_id.upper()].value
        self.call(self.vm_runvm, value)
        time.sleep(1)

    @property
    def type(self) -> str:
        """Returns the type of Voicemeeter installation (basic, banana, potato)."""
        type_ = ct.c_long()
        self.call(self.vm_get_type, ct.byref(type_))
        return KindId(type_.value).name.lower()

    @property
    def version(self) -> str:
        """Returns Voicemeeter's version as a string"""
        ver = ct.c_long()
        self.call(self.vm_get_version, ct.byref(ver))
        return "{}.{}.{}.{}".format(
            (ver.value & 0xFF000000) >> 24,
            (ver.value & 0x00FF0000) >> 16,
            (ver.value & 0x0000FF00) >> 8,
            ver.value & 0x000000FF,
        )

    @property
    def pdirty(self) -> bool:
        """True iff UI parameters have been updated."""
        return self.call(self.vm_pdirty, ok=(0, 1)) == 1

    @property
    def mdirty(self) -> bool:
        """True iff MB parameters have been updated."""
        try:
            return self.call(self.vm_mdirty, ok=(0, 1)) == 1
        except AttributeError as e:
            self.logger.exception(f"{type(e).__name__}: {e}")
            ERR_MSG = (
                "no bind for VBVMR_MacroButton_IsDirty.",
                "are you using an old version of the API?",
            )
            raise CAPIError(
                "VBVMR_MacroButton_IsDirty", -9, msg=" ".join(ERR_MSG)
            ) from e

    @property
    def ldirty(self) -> bool:
        """True iff levels have been updated."""
        self._strip_buf, self._bus_buf = self._get_levels()
        return not (
            self.cache.get("strip_level") == self._strip_buf
            and self.cache.get("bus_level") == self._bus_buf
        )

    def clear_dirty(self) -> NoReturn:
        try:
            while self.pdirty or self.mdirty:
                pass
        except CAPIError as e:
            if e.fn_name == "VBVMR_MacroButton_IsDirty" and e.code != -9:
                raise
            self.logger.error(f"{e} clearing pdirty only.")
            while self.pdirty:
                pass

    @polling
    def get(self, param: str, is_string: Optional[bool] = False) -> Union[str, float]:
        """Gets a string or float parameter"""
        if is_string:
            buf = ct.create_unicode_buffer(512)
            self.call(self.vm_get_parameter_string, param.encode(), ct.byref(buf))
        else:
            buf = ct.c_float()
            self.call(self.vm_get_parameter_float, param.encode(), ct.byref(buf))
        return buf.value

    def set(self, param: str, val: Union[str, float]) -> NoReturn:
        """Sets a string or float parameter. Caches value"""
        if isinstance(val, str):
            if len(val) >= 512:
                raise VMError("String is too long")
            self.call(self.vm_set_parameter_string, param.encode(), ct.c_wchar_p(val))
        else:
            self.call(
                self.vm_set_parameter_float, param.encode(), ct.c_float(float(val))
            )
        self.cache[param] = val

    @polling
    def get_buttonstatus(self, id: int, mode: int) -> int:
        """Gets a macrobutton parameter"""
        state = ct.c_float()
        try:
            self.call(
                self.vm_get_buttonstatus,
                ct.c_long(id),
                ct.byref(state),
                ct.c_long(mode),
            )
        except AttributeError as e:
            self.logger.exception(f"{type(e).__name__}: {e}")
            ERR_MSG = (
                "no bind for VBVMR_MacroButton_GetStatus.",
                "are you using an old version of the API?",
            )
            raise CAPIError(
                "VBVMR_MacroButton_GetStatus", -9, msg=" ".join(ERR_MSG)
            ) from e
        return int(state.value)

    def set_buttonstatus(self, id: int, state: int, mode: int) -> NoReturn:
        """Sets a macrobutton parameter. Caches value"""
        c_state = ct.c_float(float(state))
        try:
            self.call(self.vm_set_buttonstatus, ct.c_long(id), c_state, ct.c_long(mode))
        except AttributeError as e:
            self.logger.exception(f"{type(e).__name__}: {e}")
            ERR_MSG = (
                "no bind for VBVMR_MacroButton_SetStatus.",
                "are you using an old version of the API?",
            )
            raise CAPIError(
                "VBVMR_MacroButton_SetStatus", -9, msg=" ".join(ERR_MSG)
            ) from e
        self.cache[f"mb_{id}_{mode}"] = int(c_state.value)

    def get_num_devices(self, direction: str = None) -> int:
        """Retrieves number of physical devices connected"""
        if direction not in ("in", "out"):
            raise VMError("Expected a direction: in or out")
        func = getattr(self, f"vm_get_num_{direction}devices")
        res = self.call(func, ok_exp=lambda r: r >= 0)
        return res

    def get_device_description(self, index: int, direction: str = None) -> tuple:
        """Returns a tuple of device parameters"""
        if direction not in ("in", "out"):
            raise VMError("Expected a direction: in or out")
        type_ = ct.c_long()
        name = ct.create_unicode_buffer(256)
        hwid = ct.create_unicode_buffer(256)
        func = getattr(self, f"vm_get_desc_{direction}devices")
        self.call(
            func,
            ct.c_long(index),
            ct.byref(type_),
            ct.byref(name),
            ct.byref(hwid),
        )
        return (name.value, type_.value, hwid.value)

    def get_level(self, type_: int, index: int) -> float:
        """Retrieves a single level value"""
        val = ct.c_float()
        self.call(self.vm_get_level, ct.c_long(type_), ct.c_long(index), ct.byref(val))
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
        res = self.call(
            self.vm_get_midi_message,
            ct.byref(buf),
            n,
            ok=(-5, -6),  # no data received from midi device
            ok_exp=lambda r: r >= 0,
        )
        if res > 0:
            vals = tuple(
                grouper(3, (int.from_bytes(buf[i], "little") for i in range(res)))
            )
            for msg in vals:
                ch, pitch, vel = msg
                if not self.midi._channel or self.midi._channel != ch:
                    self.midi._channel = ch
                self.midi._most_recent = pitch
                self.midi._set(pitch, vel)
            return True

    @script
    def sendtext(self, script: str):
        """Sets many parameters from a script"""
        if len(script) > 48000:
            raise ValueError("Script too large, max size 48kB")
        self.call(self.vm_set_parameter_multi, script.encode())
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
            self.logger.info(f"Profile '{name}' applied!")
        except KeyError as e:
            self.logger.error(("\n").join(error_msg))
            raise VMError(("\n").join(error_msg)) from e

    def logout(self) -> NoReturn:
        """Wait for dirty parameters to clear, then logout of the API"""
        self.clear_dirty()
        time.sleep(0.1)
        self.call(self.vm_logout)
        self.logger.info(f"{type(self).__name__}: Successfully logged out of {self}")

    def end_thread(self):
        self.logger.debug("events thread shutdown started")
        self.running = False

    def __exit__(self, exc_type, exc_value, exc_traceback) -> NoReturn:
        """teardown procedures"""
        self.end_thread()
        self.logout()
