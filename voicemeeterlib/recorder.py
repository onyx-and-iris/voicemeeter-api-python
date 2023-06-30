from .error import VMError
from .iremote import IRemote
from .kinds import kinds_all
from .meta import action_fn, bool_prop


class Recorder(IRemote):
    """
    Implements the common interface

    Defines concrete implementation for recorder
    """

    @classmethod
    def make(cls, remote):
        """
        Factory function for recorder.

        Returns a Recorder class of a kind.
        """
        CHANNELOUTMIXIN_cls = _make_channelout_mixins[remote.kind.name]
        ARMSTRIPMIXIN_cls = _make_armstrip_mixins(remote)[remote.kind.name]
        REC_cls = type(
            f"Recorder{remote.kind}",
            (cls, CHANNELOUTMIXIN_cls, ARMSTRIPMIXIN_cls),
            {
                **{
                    param: action_fn(param)
                    for param in [
                        "play",
                        "stop",
                        "pause",
                        "replay",
                        "record",
                        "ff",
                        "rew",
                    ]
                },
                "mode": RecorderMode(remote),
            },
        )
        return REC_cls(remote)

    def __str__(self):
        return f"{type(self).__name__}"

    @property
    def identifier(self) -> str:
        return "recorder"

    def load(self, file: str):
        try:
            self.setter("load", file)
        except UnicodeError:
            raise VMError("File full directory must be a raw string")

    def set_loop(self, val: bool):
        self.setter("mode.loop", 1 if val else 0)

    loop = property(fset=set_loop)

    @property
    def bitresolution(self) -> int:
        set.getter("bitresolution")

    @bitresolution.setter
    def bitresolution(self, val: int):
        set.getter("bitresolution", val)

    @property
    def channel(self) -> int:
        set.getter("channel")

    @channel.setter
    def channel(self, val: int):
        set.getter("channel", val)

    @property
    def gain(self) -> float:
        return round(self.getter("gain"), 1)

    @gain.setter
    def gain(self, val: float):
        self.setter("gain", val)


class RecorderMode(IRemote):
    def identifier(self):
        return "recorder.mode"

    @property
    def recbus(self) -> bool:
        self.getter("recbus")

    @recbus.setter
    def recbus(self, val: bool):
        self.setter("recbus", 1 if val else 0)

    @property
    def playonload(self) -> bool:
        self.getter("playonload")

    @playonload.setter
    def playonload(self, val: bool):
        self.setter("playonload", 1 if val else 0)

    @property
    def loop(self) -> bool:
        self.getter("loop")

    @loop.setter
    def loop(self, val: bool):
        self.setter("recbus", 1 if val else 0)

    @property
    def multitrack(self) -> bool:
        self.getter("recbus")

    @multitrack.setter
    def multitrack(self, val: bool):
        self.setter("recbus", 1 if val else 0)


class RecorderArmStrip(IRemote):
    def __init__(self, remote, i):
        super().__init__(remote)
        self._i = i

    @property
    def identifier(self):
        return f"recorder.armstrip[{self._i}]"

    def set(self, val: bool):
        self.setter("", 1 if val else 0)


class RecorderArmBus(IRemote):
    def __init__(self, remote, i):
        super().__init__(remote)
        self._i = i

    @property
    def identifier(self):
        return f"recorder.armbus[{self._i}]"

    def set(self, val: bool):
        self.setter("", 1 if val else 0)


def _make_armstrip_mixin(remote, kind):
    return type(
        f"ArmStripMixin",
        (),
        {
            "armstrip": tuple(
                RecorderArmStrip(remote, i) for i in range(kind.num_strip)
            ),
            "armbus": tuple(RecorderArmBus(remote, i) for i in range(kind.num_bus)),
        },
    )


def _make_armstrip_mixins(remote):
    return {kind.name: _make_armstrip_mixin(remote, kind) for kind in kinds_all}


def _make_channelout_mixin(kind):
    """Creates a channel out property mixin"""
    return type(
        f"ChannelOutMixin{kind}",
        (),
        {
            **{f"A{i}": bool_prop(f"A{i}") for i in range(1, kind.phys_out + 1)},
            **{f"B{i}": bool_prop(f"B{i}") for i in range(1, kind.virt_out + 1)},
        },
    )


_make_channelout_mixins = {
    kind.name: _make_channelout_mixin(kind) for kind in kinds_all
}
