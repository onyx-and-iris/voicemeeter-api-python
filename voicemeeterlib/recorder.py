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
        ChannelMixin = _channel_mixins[remote.kind.name]
        REC_cls = type(
            f"Recorder{remote.kind}",
            (cls, ChannelMixin),
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
                        "rw",
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
        if not isinstance(val, bool) and val not in (0, 1):
            raise VMError("Error True or False expected")
        self.setter("mode.loop", 1 if val else 0)

    loop = property(fset=set_loop)


def _make_channel_mixin(kind):
    """Creates a channel out property mixin"""
    num_A, num_B = kind.outs
    return type(
        f"ChannelMixin{kind.name}",
        (),
        {
            **{f"A{i}": bool_prop(f"A{i}") for i in range(1, num_A + 1)},
            **{f"B{i}": bool_prop(f"B{i}") for i in range(1, num_B + 1)},
        },
    )


_channel_mixins = {kind.name: _make_channel_mixin(kind) for kind in kinds_all}
