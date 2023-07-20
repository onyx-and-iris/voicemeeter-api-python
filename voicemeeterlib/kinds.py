from dataclasses import dataclass
from enum import Enum, unique

from .error import VMError


@unique
class KindId(Enum):
    BASIC = 1
    BANANA = 2
    POTATO = 3


class SingletonType(type):
    """ensure only a single instance of a kind map object"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


@dataclass
class KindMapClass(metaclass=SingletonType):
    name: str
    ins: tuple
    outs: tuple
    vban: tuple
    asio: tuple
    insert: int

    @property
    def phys_in(self) -> int:
        return self.ins[0]

    @property
    def virt_in(self) -> int:
        return self.ins[-1]

    @property
    def phys_out(self) -> int:
        return self.outs[0]

    @property
    def virt_out(self) -> int:
        return self.outs[-1]

    @property
    def num_strip(self) -> int:
        return sum(self.ins)

    @property
    def num_bus(self) -> int:
        return sum(self.outs)

    @property
    def num_strip_levels(self) -> int:
        return 2 * self.phys_in + 8 * self.virt_in

    @property
    def num_bus_levels(self) -> int:
        return 8 * (self.phys_out + self.virt_out)

    def __str__(self) -> str:
        return self.name.capitalize()


@dataclass
class BasicMap(KindMapClass):
    name: str
    ins: tuple = (2, 1)
    outs: tuple = (1, 1)
    vban: tuple = (4, 4, 1, 1)
    asio: tuple = (0, 0)
    insert: int = 0


@dataclass
class BananaMap(KindMapClass):
    name: str
    ins: tuple = (3, 2)
    outs: tuple = (3, 2)
    vban: tuple = (8, 8, 1, 1)
    asio: tuple = (6, 8)
    insert: int = 22


@dataclass
class PotatoMap(KindMapClass):
    name: str
    ins: tuple = (5, 3)
    outs: tuple = (5, 3)
    vban: tuple = (8, 8, 1, 1)
    asio: tuple = (10, 8)
    insert: int = 34


def kind_factory(kind_id):
    match kind_id:
        case "basic":
            _kind_map = BasicMap
        case "banana":
            _kind_map = BananaMap
        case "potato":
            _kind_map = PotatoMap
        case _:
            raise ValueError(f"Unknown Voicemeeter kind {kind_id}")
    return _kind_map(name=kind_id)


def request_kind_map(kind_id):
    KIND_obj = None
    try:
        KIND_obj = kind_factory(kind_id)
    except ValueError as e:
        raise VMError(str(e)) from e
    return KIND_obj


kinds_all = list(request_kind_map(kind_id.name.lower()) for kind_id in KindId)
