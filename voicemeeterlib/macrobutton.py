from .error import VMError
from .iremote import IRemote


class Adapter(IRemote):
    """Adapter to the common interface."""

    def identifier(self):
        pass

    def getter(self, id, mode):
        return self._remote.get_buttonstatus(id, mode)

    def setter(self, id, val, mode):
        self._remote.set_buttonstatus(id, val, mode)


class MacroButton(Adapter):
    """Defines concrete implementation for macrobutton"""

    def __str__(self):
        return f"{type(self).__name__}{self._remote.kind}{self.index}"

    @property
    def state(self) -> bool:
        return self.getter(self.index, 1) == 1

    @state.setter
    def state(self, val):
        if not isinstance(val, bool) and val not in (0, 1):
            raise VMError("state is a boolean parameter")
        self.setter(self.index, 1 if val else 0, 1)

    @property
    def stateonly(self) -> bool:
        return self.getter(self.index, 2) == 1

    @stateonly.setter
    def stateonly(self, val):
        if not isinstance(val, bool) and val not in (0, 1):
            raise VMError("stateonly is a boolean parameter")
        self.setter(self.index, 1 if val else 0, 2)

    @property
    def trigger(self) -> bool:
        return self.getter(self.index, 3) == 1

    @trigger.setter
    def trigger(self, val):
        if not isinstance(val, bool) and val not in (0, 1):
            raise VMError("trigger is a boolean parameter")
        self.setter(self.index, 1 if val else 0, 3)
