from .error import VMError
from .iremote import IRemote
from .meta import action_prop


class Command(IRemote):
    """
    Implements the common interface

    Defines concrete implementation for command
    """

    @classmethod
    def make(cls, remote):
        """
        Factory function for command class.

        Returns a Command class of a kind.
        """
        CMD_cls = type(
            f"Command{remote.kind}",
            (cls,),
            {
                **{
                    param: action_prop(param)
                    for param in ["show", "shutdown", "restart"]
                },
                "hide": action_prop("show", val=0),
            },
        )
        return CMD_cls(remote)

    def __str__(self):
        return f"{type(self).__name__}"

    @property
    def identifier(self) -> str:
        return "Command"

    def set_showvbanchat(self, val: bool):
        if not isinstance(val, bool) and val not in (0, 1):
            raise VMError("showvbanchat is a boolean parameter")
        self.setter("DialogShow.VBANCHAT", 1 if val else 0)

    showvbanchat = property(fset=set_showvbanchat)

    def set_lock(self, val: bool):
        if not isinstance(val, bool) and val not in (0, 1):
            raise VMError("lock is a boolean parameter")
        self.setter("lock", 1 if val else 0)

    lock = property(fset=set_lock)

    def reset(self):
        self._remote.apply_config("reset")
