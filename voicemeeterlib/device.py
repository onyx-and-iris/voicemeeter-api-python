from abc import abstractmethod
from typing import Union

from .iremote import IRemote


class Adapter(IRemote):
    """Adapter to the common interface."""

    @abstractmethod
    def ins(self):
        pass

    @abstractmethod
    def outs(self):
        pass

    @abstractmethod
    def input(self):
        pass

    @abstractmethod
    def output(self):
        pass

    def identifier(self):
        pass

    def getter(self, index: int = None, direction: str = None) -> Union[int, dict]:
        if index is None:
            return self._remote.get_num_devices(direction)

        vals = self._remote.get_device_description(index, direction)
        types = {1: "mme", 3: "wdm", 4: "ks", 5: "asio"}
        return {"name": vals[0], "type": types[vals[1]], "id": vals[2]}


class Device(Adapter):
    """Defines concrete implementation for device"""

    @classmethod
    def make(cls, remote):
        """
        Factory function for device.

        Returns a Device class of a kind.
        """

        def num_ins(cls) -> int:
            return cls.getter(direction="in")

        def num_outs(cls) -> int:
            return cls.getter(direction="out")

        DEVICE_cls = type(
            f"Device{remote.kind}",
            (cls,),
            {
                "ins": property(num_ins),
                "outs": property(num_outs),
            },
        )
        return DEVICE_cls(remote)

    def __str__(self):
        return f"{type(self).__name__}"

    def input(self, index: int) -> dict:
        return self.getter(index=index, direction="in")

    def output(self, index: int) -> dict:
        return self.getter(index=index, direction="out")
