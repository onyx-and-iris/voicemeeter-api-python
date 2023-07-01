import re

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
        ARMCHANNELMIXIN_cls = _make_armchannel_mixins(remote)[remote.kind.name]
        REC_cls = type(
            f"Recorder{remote.kind}",
            (cls, CHANNELOUTMIXIN_cls, ARMCHANNELMIXIN_cls),
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

    @property
    def samplerate(self) -> int:
        return int(self.getter("samplerate"))

    @samplerate.setter
    def samplerate(self, val: int):
        opts = (22050, 24000, 32000, 44100, 48000, 88200, 96000, 176400, 192000)
        if val not in opts:
            self.logger.warning(f"samplerate got: {val} but expected a value in {opts}")
        self.setter("samplerate", val)

    @property
    def bitresolution(self) -> int:
        return int(self.getter("bitresolution"))

    @bitresolution.setter
    def bitresolution(self, val: int):
        opts = (8, 16, 24, 32)
        if val not in opts:
            self.logger.warning(
                f"bitresolution got: {val} but expected a value in {opts}"
            )
        self.setter("bitresolution", val)

    @property
    def channel(self) -> int:
        return int(self.getter("channel"))

    @channel.setter
    def channel(self, val: int):
        if not 1 <= val <= 8:
            self.logger.warning(f"channel got: {val} but expected a value from 1 to 8")
        self.setter("channel", val)

    @property
    def kbps(self):
        return int(self.getter("kbps"))

    @kbps.setter
    def kbps(self, val: int):
        opts = (32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320)
        if val not in opts:
            self.logger.warning(f"kbps got: {val} but expected a value in {opts}")
        self.setter("kbps", val)

    @property
    def gain(self) -> float:
        return round(self.getter("gain"), 1)

    @gain.setter
    def gain(self, val: float):
        self.setter("gain", val)

    def load(self, file: str):
        try:
            self.setter("load", file)
        except UnicodeError:
            raise VMError("File full directory must be a raw string")

    # loop forwarder methods, for backwards compatibility
    @property
    def loop(self):
        return self.mode.loop

    @loop.setter
    def loop(self, val: bool):
        self.mode.loop = val

    def goto(self, time_str):
        def get_sec():
            """Get seconds from time string"""
            h, m, s = time_str.split(":")
            return int(h) * 3600 + int(m) * 60 + int(s)

        time_str = str(time_str)  # coerce the type
        if (
            match := re.match(
                r"^(?:[01]\d|2[0123]):(?:[012345]\d):(?:[012345]\d)$",
                time_str,
            )
            is not None
        ):
            self.setter("goto", get_sec())
        else:
            self.logger.warning(
                f"goto expects a string that matches the format 'hh:mm:ss'"
            )

    def filetype(self, val: str):
        opts = {"wav": 1, "aiff": 2, "bwf": 3, "mp3": 100}
        try:
            self.setter("filetype", opts[val.lower()])
        except KeyError:
            self.logger.warning(
                f"filetype got: {val} but expected a value in {list(opts.keys())}"
            )


class RecorderMode(IRemote):
    @property
    def identifier(self):
        return "recorder.mode"

    @property
    def recbus(self) -> bool:
        return self.getter("recbus") == 1

    @recbus.setter
    def recbus(self, val: bool):
        self.setter("recbus", 1 if val else 0)

    @property
    def playonload(self) -> bool:
        return self.getter("playonload") == 1

    @playonload.setter
    def playonload(self, val: bool):
        self.setter("playonload", 1 if val else 0)

    @property
    def loop(self) -> bool:
        return self.getter("loop") == 1

    @loop.setter
    def loop(self, val: bool):
        self.setter("loop", 1 if val else 0)

    @property
    def multitrack(self) -> bool:
        return self.getter("multitrack") == 1

    @multitrack.setter
    def multitrack(self, val: bool):
        self.setter("multitrack", 1 if val else 0)


class RecorderArmChannel(IRemote):
    def __init__(self, remote, i):
        super().__init__(remote)
        self._i = i

    def set(self, val: bool):
        self.setter("", 1 if val else 0)


class RecorderArmStrip(RecorderArmChannel):
    @property
    def identifier(self):
        return f"recorder.armstrip[{self._i}]"


class RecorderArmBus(RecorderArmChannel):
    @property
    def identifier(self):
        return f"recorder.armbus[{self._i}]"


def _make_armchannel_mixin(remote, kind):
    """Creates an armchannel out mixin"""
    return type(
        f"ArmChannelMixin{kind}",
        (),
        {
            "armstrip": tuple(
                RecorderArmStrip(remote, i) for i in range(kind.num_strip)
            ),
            "armbus": tuple(RecorderArmBus(remote, i) for i in range(kind.num_bus)),
        },
    )


def _make_armchannel_mixins(remote):
    return {kind.name: _make_armchannel_mixin(remote, kind) for kind in kinds_all}


def _make_channelout_mixin(kind):
    """Creates a channel out mixin"""
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
