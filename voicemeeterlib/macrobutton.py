from .error import VMError
from .iremote import IRemote


class Adapter(IRemote):
    """Adapter to the common interface."""

    def identifier(self):
        pass

    def getter(self, mode):
        return self._remote.get_buttonstatus(self.index, mode)

    def setter(self, val, mode):
        self._remote.set_buttonstatus(self.index, val, mode)


class MacroButton(Adapter):
    """Defines concrete implementation for macrobutton"""

    def __str__(self):
        return f"{type(self).__name__}{self._remote.kind}{self.index}"

    @property
    def state(self) -> bool:
        return self.getter(1) == 1

    @state.setter
    def state(self, val):
        self.setter(1 if val else 0, 1)

    @property
    def stateonly(self) -> bool:
        return self.getter(2) == 1

    @stateonly.setter
    def stateonly(self, val):
        self.setter(1 if val else 0, 2)

    @property
    def trigger(self) -> bool:
        return self.getter(3) == 1

    @trigger.setter
    def trigger(self, val):
        self.setter(1 if val else 0, 3)
