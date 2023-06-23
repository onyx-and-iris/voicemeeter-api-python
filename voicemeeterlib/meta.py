def bool_prop(param):
    """meta function for boolean parameters"""

    def fget(self) -> bool:
        return self.getter(param) == 1

    def fset(self, val: bool):
        self.setter(param, 1 if val else 0)

    return property(fget, fset)


def float_prop(param):
    """meta function for float parameters"""

    def fget(self):
        return self.getter(param)

    def fset(self, val):
        self.setter(param, val)

    return property(fget, fset)


def action_fn(param, val: int = 1):
    """meta function that performs an action"""

    def fdo(self):
        self.setter(param, val)

    return fdo


def bus_mode_prop(param):
    """meta function for bus mode parameters"""

    def fget(self) -> bool:
        self._remote.clear_dirty()
        return self.getter(param) == 1

    def fset(self, val: bool):
        self.setter(param, 1 if val else 0)

    return property(fget, fset)


def device_prop(param):
    """meta function for strip device parameters"""

    def fset(self, val: str):
        self.setter(param, val)

    return property(fset=fset)
