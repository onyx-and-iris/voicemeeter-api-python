import logging
import time
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)


class IRemote(metaclass=ABCMeta):
    """
    Common interface between base class and extended (higher) classes

    Provides some default implementation
    """

    def __init__(self, remote, index=None):
        self._remote = remote
        self.index = index
        self.logger = logger.getChild(self.__class__.__name__)

    def getter(self, param, **kwargs):
        """Gets a parameter value"""
        self.logger.debug(f"getter: {self._cmd(param)}")
        return self._remote.get(self._cmd(param), **kwargs)

    def setter(self, param, val):
        """Sets a parameter value"""
        self.logger.debug(f"setter: {self._cmd(param)}={val}")
        self._remote.set(self._cmd(param), val)

    def _cmd(self, param):
        cmd = (self.identifier,)
        if param:
            cmd += (f".{param}",)
        return "".join(cmd)

    @abstractmethod
    def identifier(self):
        pass

    def apply(self, data: dict):
        def fget(attr, val):
            if attr == "mode":
                return (getattr(self, attr), val, 1)
            return (self, attr, val)

        for attr, val in data.items():
            if not isinstance(val, dict):
                if attr in dir(self):  # avoid calling getattr (with hasattr)
                    target, attr, val = fget(attr, val)
                    setattr(target, attr, val)
                else:
                    self.logger.error(f"invalid attribute {attr} for {self}")
            else:
                target = getattr(self, attr)
                target.apply(val)
        return self

    def then_wait(self):
        time.sleep(self._remote.DELAY)
