from .error import VMError
from .iremote import IRemote
from .kinds import kinds_all
from .meta import action_prop, bool_prop


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
        REC_cls = type(
            f"Recorder{remote.kind}",
            (cls, CHANNELOUTMIXIN_cls),
            {
                **{
                    param: action_prop(param)
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
