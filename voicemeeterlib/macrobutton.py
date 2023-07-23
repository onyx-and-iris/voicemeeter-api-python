from enum import IntEnum

from .iremote import IRemote

ButtonModes = IntEnum(
    "ButtonModes",
    "state stateonly trigger",
    start=1,
)


class Adapter(IRemote):
    """Adapter to the common interface."""

    def getter(self, mode):
        self.logger.debug(f"getter: button[{self.index}].{ButtonModes(mode).name}")
        return self._remote.get_buttonstatus(self.index, mode)

    def setter(self, mode, val):
        self.logger.debug(
            f"setter: button[{self.index}].{ButtonModes(mode).name}={val}"
        )
        self._remote.set_buttonstatus(self.index, val, mode)


class MacroButtonColorMixin(IRemote):
    @property
    def identifier(self):
        return f"command.button[{self.index}]"

    @property
    def color(self) -> int:
        return int(IRemote.getter(self, "color"))

    @color.setter
    def color(self, val: int):
        IRemote.setter(self, "color", val)


class MacroButton(Adapter, MacroButtonColorMixin):
    """Defines concrete implementation for macrobutton"""

    def __str__(self):
        return f"{type(self).__name__}{self._remote.kind}{self.index}"

    @property
    def state(self) -> bool:
        return self.getter(ButtonModes.state) == 1

    @state.setter
    def state(self, val: bool):
        self.setter(ButtonModes.state, 1 if val else 0)

    @property
    def stateonly(self) -> bool:
        return self.getter(ButtonModes.stateonly) == 1

    @stateonly.setter
    def stateonly(self, val: bool):
        self.setter(ButtonModes.stateonly, 1 if val else 0)

    @property
    def trigger(self) -> bool:
        return self.getter(ButtonModes.trigger) == 1

    @trigger.setter
    def trigger(self, val: bool):
        self.setter(ButtonModes.trigger, 1 if val else 0)
