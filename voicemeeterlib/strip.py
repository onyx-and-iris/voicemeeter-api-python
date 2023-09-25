import time
from abc import abstractmethod
from math import log
from typing import Union

from .iremote import IRemote
from .kinds import kinds_all
from .meta import bool_prop, device_prop, float_prop


class Strip(IRemote):
    """
    Implements the common interface

    Defines concrete implementation for strip
    """

    @abstractmethod
    def __str__(self):
        pass

    @property
    def identifier(self) -> str:
        return f"strip[{self.index}]"

    @property
    def mono(self) -> bool:
        return self.getter("mono") == 1

    @mono.setter
    def mono(self, val: bool):
        self.setter("mono", 1 if val else 0)

    @property
    def solo(self) -> bool:
        return self.getter("solo") == 1

    @solo.setter
    def solo(self, val: bool):
        self.setter("solo", 1 if val else 0)

    @property
    def mute(self) -> bool:
        return self.getter("mute") == 1

    @mute.setter
    def mute(self, val: bool):
        self.setter("mute", 1 if val else 0)

    @property
    def limit(self) -> int:
        return int(self.getter("limit"))

    @limit.setter
    def limit(self, val: int):
        self.setter("limit", val)

    @property
    def label(self) -> str:
        return self.getter("Label", is_string=True)

    @label.setter
    def label(self, val: str):
        self.setter("Label", str(val))

    @property
    def gain(self) -> float:
        return round(self.getter("gain"), 1)

    @gain.setter
    def gain(self, val: float):
        self.setter("gain", val)

    def fadeto(self, target: float, time_: int):
        self.setter("FadeTo", f"({target}, {time_})")
        time.sleep(self._remote.DELAY)

    def fadeby(self, change: float, time_: int):
        self.setter("FadeBy", f"({change}, {time_})")
        time.sleep(self._remote.DELAY)


class PhysicalStrip(Strip):
    @classmethod
    def make(cls, remote, i, is_phys):
        """
        Factory method for PhysicalStrip.

        Returns a PhysicalStrip class.
        """
        EFFECTS_cls = _make_effects_mixins(is_phys)[remote.kind.name]
        return type(
            f"PhysicalStrip",
            (cls, EFFECTS_cls),
            {
                "comp": StripComp(remote, i),
                "gate": StripGate(remote, i),
                "denoiser": StripDenoiser(remote, i),
                "eq": StripEQ(remote, i),
                "device": StripDevice.make(remote, i),
            },
        )

    def __str__(self):
        return f"{type(self).__name__}{self.index}"

    @property
    def audibility(self) -> float:
        return round(self.getter("audibility"), 1)

    @audibility.setter
    def audibility(self, val: float):
        self.setter("audibility", val)


class StripComp(IRemote):
    @property
    def identifier(self) -> str:
        return f"Strip[{self.index}].comp"

    @property
    def knob(self) -> float:
        return round(self.getter(""), 1)

    @knob.setter
    def knob(self, val: float):
        self.setter("", val)

    @property
    def gainin(self) -> float:
        return round(self.getter("GainIn"), 1)

    @gainin.setter
    def gainin(self, val: float):
        self.setter("GainIn", val)

    @property
    def ratio(self) -> float:
        return round(self.getter("Ratio"), 1)

    @ratio.setter
    def ratio(self, val: float):
        self.setter("Ratio", val)

    @property
    def threshold(self) -> float:
        return round(self.getter("Threshold"), 1)

    @threshold.setter
    def threshold(self, val: float):
        self.setter("Threshold", val)

    @property
    def attack(self) -> float:
        return round(self.getter("Attack"), 1)

    @attack.setter
    def attack(self, val: float):
        self.setter("Attack", val)

    @property
    def release(self) -> float:
        return round(self.getter("Release"), 1)

    @release.setter
    def release(self, val: float):
        self.setter("Release", val)

    @property
    def knee(self) -> float:
        return round(self.getter("Knee"), 2)

    @knee.setter
    def knee(self, val: float):
        self.setter("Knee", val)

    @property
    def gainout(self) -> float:
        return round(self.getter("GainOut"), 1)

    @gainout.setter
    def gainout(self, val: float):
        self.setter("GainOut", val)

    @property
    def makeup(self) -> bool:
        return self.getter("makeup") == 1

    @makeup.setter
    def makeup(self, val: bool):
        self.setter("makeup", 1 if val else 0)


class StripGate(IRemote):
    @property
    def identifier(self) -> str:
        return f"Strip[{self.index}].gate"

    @property
    def knob(self) -> float:
        return round(self.getter(""), 1)

    @knob.setter
    def knob(self, val: float):
        self.setter("", val)

    @property
    def threshold(self) -> float:
        return round(self.getter("Threshold"), 1)

    @threshold.setter
    def threshold(self, val: float):
        self.setter("Threshold", val)

    @property
    def damping(self) -> float:
        return round(self.getter("Damping"), 1)

    @damping.setter
    def damping(self, val: float):
        self.setter("Damping", val)

    @property
    def bpsidechain(self) -> int:
        return int(self.getter("BPSidechain"))

    @bpsidechain.setter
    def bpsidechain(self, val: int):
        self.setter("BPSidechain", val)

    @property
    def attack(self) -> float:
        return round(self.getter("Attack"), 1)

    @attack.setter
    def attack(self, val: float):
        self.setter("Attack", val)

    @property
    def hold(self) -> float:
        return round(self.getter("Hold"), 1)

    @hold.setter
    def hold(self, val: float):
        self.setter("Hold", val)

    @property
    def release(self) -> float:
        return round(self.getter("Release"), 1)

    @release.setter
    def release(self, val: float):
        self.setter("Release", val)


class StripDenoiser(IRemote):
    @property
    def identifier(self) -> str:
        return f"Strip[{self.index}].denoiser"

    @property
    def knob(self) -> float:
        return round(self.getter(""), 1)

    @knob.setter
    def knob(self, val: float):
        self.setter("", val)


class StripEQ(IRemote):
    @property
    def identifier(self) -> str:
        return f"Strip[{self.index}].eq"

    @property
    def on(self) -> bool:
        return self.getter("on") == 1

    @on.setter
    def on(self, val: bool):
        self.setter("on", 1 if val else 0)

    @property
    def ab(self) -> bool:
        return self.getter("ab") == 1

    @ab.setter
    def ab(self, val: bool):
        self.setter("ab", 1 if val else 0)


class StripDevice(IRemote):
    @classmethod
    def make(cls, remote, i):
        """
        Factory function for strip.device.

        Returns a StripDevice class of a kind.
        """
        DEVICE_cls = type(
            f"StripDevice{remote.kind}",
            (cls,),
            {
                **{
                    param: device_prop(param)
                    for param in [
                        "wdm",
                        "ks",
                        "mme",
                        "asio",
                    ]
                },
            },
        )
        return DEVICE_cls(remote, i)

    @property
    def identifier(self) -> str:
        return f"Strip[{self.index}].device"

    @property
    def name(self) -> str:
        return self.getter("name", is_string=True)

    @property
    def sr(self) -> int:
        return int(self.getter("sr"))


class VirtualStrip(Strip):
    @classmethod
    def make(cls, remote, i, is_phys):
        """
        Factory method for VirtualStrip.

        Returns a VirtualStrip class.
        """
        EFFECTS_cls = _make_effects_mixins(is_phys)[remote.kind.name]
        return type(
            f"VirtualStrip",
            (cls, EFFECTS_cls),
            {},
        )

    def __str__(self):
        return f"{type(self).__name__}{self.index}"

    @property
    def mc(self) -> bool:
        return self.getter("mc") == 1

    @mc.setter
    def mc(self, val: bool):
        self.setter("mc", 1 if val else 0)

    mono = mc

    @property
    def k(self) -> int:
        return int(self.getter("karaoke"))

    @k.setter
    def k(self, val: int):
        self.setter("karaoke", val)

    @property
    def bass(self) -> float:
        return round(self.getter("EQGain1"), 1)

    @bass.setter
    def bass(self, val: float):
        self.setter("EQGain1", val)

    @property
    def mid(self) -> float:
        return round(self.getter("EQGain2"), 1)

    @mid.setter
    def mid(self, val: float):
        self.setter("EQGain2", val)

    med = mid

    @property
    def treble(self) -> float:
        return round(self.getter("EQGain3"), 1)

    high = treble

    @treble.setter
    def treble(self, val: float):
        self.setter("EQGain3", val)

    def appgain(self, name: str, gain: float):
        self.setter("AppGain", f'("{name}", {gain})')

    def appmute(self, name: str, mute: bool = None):
        self.setter("AppMute", f'("{name}", {1 if mute else 0})')


class StripLevel(IRemote):
    def __init__(self, remote, index):
        super().__init__(remote, index)
        self.range = _make_strip_level_maps[remote.kind.name][self.index]

    def getter(self, mode):
        """
        Returns a tuple of level values for the channel.

        If observables thread running and level updates are subscribed to, fetch values from cache

        Otherwise call CAPI func.
        """

        def fget(x):
            return round(20 * log(x, 10), 1) if x > 0 else -200.0

        if not self._remote.stopped() and self._remote.event.ldirty:
            vals = self._remote.cache["strip_level"][self.range[0] : self.range[-1]]
        else:
            vals = [self._remote.get_level(mode, i) for i in range(*self.range)]

        return tuple(fget(val) for val in vals)

    @property
    def identifier(self) -> str:
        return f"Strip[{self.index}]"

    @property
    def prefader(self) -> tuple:
        self._remote.strip_mode = 0
        return self.getter(0)

    @property
    def postfader(self) -> tuple:
        self._remote.strip_mode = 1
        return self.getter(1)

    @property
    def postmute(self) -> tuple:
        self._remote.strip_mode = 2
        return self.getter(2)

    @property
    def isdirty(self) -> bool:
        """
        Returns dirty status for this specific channel.

        Expected to be used in a callback only.
        """
        if not self._remote.stopped():
            return any(self._remote._strip_comp[self.range[0] : self.range[-1]])

    is_updated = isdirty


def make_strip_level_map(kind):
    phys_map = tuple((i, i + 2) for i in range(0, kind.phys_in * 2, 2))
    virt_map = tuple(
        (i, i + 8)
        for i in range(
            kind.phys_in * 2,
            kind.phys_in * 2 + kind.virt_in * 8,
            8,
        )
    )
    return phys_map + virt_map


_make_strip_level_maps = {kind.name: make_strip_level_map(kind) for kind in kinds_all}


class GainLayer(IRemote):
    def __init__(self, remote, index, i):
        super().__init__(remote, index)
        self._i = i

    @property
    def identifier(self) -> str:
        return f"Strip[{self.index}]"

    @property
    def gain(self):
        return self.getter(f"GainLayer[{self._i}]")

    @gain.setter
    def gain(self, val):
        self.setter(f"GainLayer[{self._i}]", val)


def _make_gainlayer_mixin(remote, index):
    """Creates a GainLayer mixin"""
    return type(
        f"GainlayerMixin",
        (),
        {
            "gainlayer": tuple(
                GainLayer(remote, index, i) for i in range(remote.kind.num_bus)
            )
        },
    )


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


def _make_effects_mixin(kind, is_phys):
    """creates an effects mixin for a kind"""

    def _make_xy_cls():
        pan = {param: float_prop(param) for param in ["pan_x", "pan_y"]}
        color = {param: float_prop(param) for param in ["color_x", "color_y"]}
        fx = {param: float_prop(param) for param in ["fx_x", "fx_y"]}
        if is_phys:
            return type(
                "XYPhys",
                (),
                {
                    **pan,
                    **color,
                    **fx,
                },
            )
        return type(
            "XYVirt",
            (),
            {**pan},
        )

    def _make_fx_cls():
        if is_phys:
            return type(
                "FX",
                (),
                {
                    **{
                        param: float_prop(param)
                        for param in ["reverb", "delay", "fx1", "fx2"]
                    },
                    **{
                        f"post{param}": bool_prop(f"post{param}")
                        for param in ["reverb", "delay", "fx1", "fx2"]
                    },
                },
            )
        return type("FX", (), {})

    if kind.name == "basic":
        steps = (_make_xy_cls,)
    elif kind.name == "banana":
        steps = (_make_xy_cls,)
    elif kind.name == "potato":
        steps = (_make_xy_cls, _make_fx_cls)
    return type(f"Effects{kind}", tuple(step() for step in steps), {})


def _make_effects_mixins(is_phys):
    return {kind.name: _make_effects_mixin(kind, is_phys) for kind in kinds_all}


def strip_factory(is_phys_strip, remote, i) -> Union[PhysicalStrip, VirtualStrip]:
    """
    Factory method for strips

    Mixes in required classes

    Returns a physical or virtual strip subclass
    """
    STRIP_cls = (
        PhysicalStrip.make(remote, i, is_phys_strip)
        if is_phys_strip
        else VirtualStrip.make(remote, i, is_phys_strip)
    )
    CHANNELOUTMIXIN_cls = _make_channelout_mixins[remote.kind.name]

    _kls = (STRIP_cls, CHANNELOUTMIXIN_cls)
    if remote.kind.name == "potato":
        GAINLAYERMIXIN_cls = _make_gainlayer_mixin(remote, i)
        _kls += (GAINLAYERMIXIN_cls,)
    return type(
        f"{STRIP_cls.__name__}{remote.kind}",
        _kls,
        {
            "levels": StripLevel(remote, i),
        },
    )(remote, i)


def request_strip_obj(is_phys_strip, remote, i) -> Strip:
    """
    Strip entry point. Wraps factory method.

    Returns a reference to a strip subclass of a kind
    """
    return strip_factory(is_phys_strip, remote, i)
