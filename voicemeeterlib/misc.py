from typing import Optional

from .error import VMError
from .iremote import IRemote
from .kinds import kinds_all


class FX(IRemote):
    def __str__(self):
        return f"{type(self).__name__}"

    @property
    def identifier(self) -> str:
        return "FX"

    @property
    def reverb(self) -> bool:
        return self.getter("reverb.On") == 1

    @reverb.setter
    def reverb(self, val: bool):
        self.setter("reverb.On", 1 if val else 0)

    @property
    def reverb_ab(self) -> bool:
        return self.getter("reverb.ab") == 1

    @reverb_ab.setter
    def reverb_ab(self, val: bool):
        self.setter("reverb.ab", 1 if val else 0)

    @property
    def delay(self) -> bool:
        return self.getter("delay.On") == 1

    @delay.setter
    def delay(self, val: bool):
        self.setter("delay.On", 1 if val else 0)

    @property
    def delay_ab(self) -> bool:
        return self.getter("delay.ab") == 1

    @delay_ab.setter
    def delay_ab(self, val: bool):
        self.setter("delay.ab", 1 if val else 0)


class Patch(IRemote):
    @classmethod
    def make(cls, remote):
        """
        Factory method for Patch.

        Mixes in required classes.

        Returns a Patch class of a kind.
        """
        ASIO_cls = _make_asio_mixins(remote)[remote.kind.name]
        return type(
            f"Patch{remote.kind}",
            (cls, ASIO_cls),
            {
                "composite": tuple(Composite(remote, i) for i in range(8)),
                "insert": tuple(Insert(remote, i) for i in range(remote.kind.insert)),
            },
        )(remote)

    def __str__(self):
        return f"{type(self).__name__}"

    @property
    def identifier(self) -> str:
        return f"patch"

    @property
    def postfadercomp(self) -> bool:
        return self.getter("postfadercomposite") == 1

    @postfadercomp.setter
    def postfadercomp(self, val: bool):
        self.setter("postfadercomposite", 1 if val else 0)

    @property
    def postfxinsert(self) -> bool:
        return self.getter("postfxinsert") == 1

    @postfxinsert.setter
    def postfxinsert(self, val: bool):
        self.setter("postfxinsert", 1 if val else 0)


class Asio(IRemote):
    @property
    def identifier(self) -> str:
        return f"patch"


class AsioIn(Asio):
    def get(self) -> int:
        return int(self.getter(f"asio[{self.index}]"))

    def set(self, val: int):
        self.setter(f"asio[{self.index}]", val)


class AsioOut(Asio):
    def __init__(self, remote, i, param):
        IRemote.__init__(self, remote, i)
        self._param = param

    def get(self) -> int:
        return int(self.getter(f"out{self._param}[{self.index}]"))

    def set(self, val: int):
        self.setter(f"out{self._param}[{self.index}]", val)


def _make_asio_mixin(remote, kind):
    """Creates an ASIO mixin for a kind"""
    asio_in, asio_out = kind.asio

    return type(
        f"ASIO{kind}",
        (IRemote,),
        {
            "asio": tuple(AsioIn(remote, i) for i in range(asio_in)),
            **{
                param: tuple(AsioOut(remote, i, param) for i in range(asio_out))
                for param in ["A2", "A3", "A4", "A5"]
            },
        },
    )


def _make_asio_mixins(remote):
    return {kind.name: _make_asio_mixin(remote, kind) for kind in kinds_all}


class Composite(IRemote):
    @property
    def identifier(self) -> str:
        return "patch"

    def get(self) -> int:
        return int(self.getter(f"composite[{self.index}]"))

    def set(self, val: int):
        self.setter(f"composite[{self.index}]", val)


class Insert(IRemote):
    @property
    def identifier(self) -> str:
        return "patch"

    @property
    def on(self) -> bool:
        return self.getter(f"insert[{self.index}]") == 1

    @on.setter
    def on(self, val: bool):
        self.setter(f"insert[{self.index}]", 1 if val else 0)


class Option(IRemote):
    @classmethod
    def make(cls, remote):
        """
        Factory method for Option.

        Mixes in required classes.

        Returns a Option class of a kind.
        """
        return type(
            f"Option{remote.kind}",
            (cls,),
            {
                "delay": tuple(Delay(remote, i) for i in range(remote.kind.phys_out)),
            },
        )(remote)

    def __str__(self):
        return f"{type(self).__name__}"

    @property
    def identifier(self) -> str:
        return "option"

    @property
    def sr(self) -> int:
        return int(self.getter("sr"))

    @sr.setter
    def sr(self, val: int):
        opts = (44100, 48000, 88200, 96000, 176400, 192000)
        if val not in opts:
            raise VMError(f"Expected one of: {opts}")
        self.setter("sr", val)

    @property
    def asiosr(self) -> bool:
        return self.getter("asiosr") == 1

    @asiosr.setter
    def asiosr(self, val: bool):
        self.setter("asiosr", 1 if val else 0)

    @property
    def monitoronsel(self) -> bool:
        return self.getter("monitoronsel") == 1

    @monitoronsel.setter
    def monitoronsel(self, val: bool):
        self.setter("monitoronsel", 1 if val else 0)

    def buffer(self, driver, buffer):
        self.setter(f"buffer.{driver}", buffer)


class Delay(IRemote):
    @property
    def identifier(self) -> str:
        return "option"

    def get(self) -> int:
        return int(self.getter(f"delay[{self.index}]"))

    def set(self, val: int):
        self.setter(f"delay[{self.index}]", val)


class Midi:
    def __init__(self):
        self._channel = None
        self.cache = {}
        self._most_recent = None

    @property
    def channel(self) -> int:
        return self._channel

    @property
    def current(self) -> int:
        return self._most_recent

    def get(self, key: int) -> Optional[int]:
        return self.cache.get(key)

    def _set(self, key: int, velocity: int):
        self.cache[key] = velocity


class Event:
    def __init__(self, subs: dict):
        self.subs = subs

    def info(self, msg):
        info = (
            f"{msg} events",
            f"Now listening for {', '.join(self.get())} events",
        )
        print("\n".join(info))

    @property
    def pdirty(self):
        return self.subs["pdirty"]

    @property
    def mdirty(self):
        return self.subs["mdirty"]

    @property
    def midi(self):
        return self.subs["midi"]

    @property
    def ldirty(self):
        return self.subs["ldirty"]

    def get(self) -> list:
        return [k for k, v in self.subs.items() if v]

    def any(self) -> bool:
        return any(self.subs.values())

    def add(self, event):
        self.subs[event] = True
        self.info(f"{event} added to")

    def remove(self, event):
        self.subs[event] = False
        self.info(f"{event} removed from")
