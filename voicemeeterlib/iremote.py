import time
from abc import ABCMeta, abstractmethod
from typing import Self


class IRemote(metaclass=ABCMeta):
    """
    Common interface between base class and extended (higher) classes

    Provides some default implementation
    """

    def __init__(self, remote, index=None):
        self._remote = remote
        self.index = index

    def getter(self, param, **kwargs):
        """Gets a parameter value"""
        return self._remote.get(f"{self.identifier}.{param}", **kwargs)

    def setter(self, param, val):
        """Sets a parameter value"""
        self._remote.set(f"{self.identifier}.{param}", val)

    @abstractmethod
    def identifier(self):
        pass

    def apply(self, data: dict) -> Self:
        def fget(attr, val):
            if attr == "mode":
                return (getattr(self, attr), val, 1)
            return (self, attr, val)

        for attr, val in data.items():
            if hasattr(self, attr):
                target, attr, val = fget(attr, val)
                setattr(target, attr, val)
        return self

    def then_wait(self):
        time.sleep(self._remote.DELAY)
