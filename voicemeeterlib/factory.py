from abc import abstractmethod
from enum import IntEnum
from functools import cached_property
from typing import Iterable, NoReturn, Self

from . import misc
from .base import Remote
from .bus import request_bus_obj as bus
from .command import Command
from .config import request_config as configs
from .device import Device
from .kinds import KindMapClass
from .kinds import request_kind_map as kindmap
from .macrobutton import MacroButton
from .recorder import Recorder
from .strip import request_strip_obj as strip
from .vban import request_vban_obj as vban


class FactoryBuilder:
    """
    Builder class for factories.

    Separates construction from representation.
    """

    BuilderProgress = IntEnum(
        "BuilderProgress",
        "strip bus command macrobutton vban device option recorder patch fx",
        start=0,
    )

    def __init__(self, factory, kind: KindMapClass):
        self._factory = factory
        self.kind = kind
        self._info = (
            f"Finished building strips for {self._factory}",
            f"Finished building buses for {self._factory}",
            f"Finished building commands for {self._factory}",
            f"Finished building macrobuttons for {self._factory}",
            f"Finished building vban in/out streams for {self._factory}",
            f"Finished building device for {self._factory}",
            f"Finished building option for {self._factory}",
            f"Finished building recorder for {self._factory}",
            f"Finished building patch for {self._factory}",
            f"Finished building fx for {self._factory}",
        )

    def _pinfo(self, name: str) -> NoReturn:
        """prints progress status for each step"""
        name = name.split("_")[1]
        print(self._info[int(getattr(self.BuilderProgress, name))])

    def make_strip(self) -> Self:
        self._factory.strip = tuple(
            strip(i < self.kind.phys_in, self._factory, i)
            for i in range(self.kind.num_strip)
        )
        return self

    def make_bus(self) -> Self:
        self._factory.bus = tuple(
            bus(i < self.kind.phys_out, self._factory, i)
            for i in range(self.kind.num_bus)
        )
        return self

    def make_command(self) -> Self:
        self._factory.command = Command.make(self._factory)
        return self

    def make_macrobutton(self) -> Self:
        self._factory.button = tuple(MacroButton(self._factory, i) for i in range(80))
        return self

    def make_vban(self) -> Self:
        self._factory.vban = vban(self._factory)
        return self

    def make_device(self) -> Self:
        self._factory.device = Device.make(self._factory)
        return self

    def make_option(self) -> Self:
        self._factory.option = misc.Option.make(self._factory)
        return self

    def make_recorder(self) -> Self:
        self._factory.recorder = Recorder.make(self._factory)
        return self

    def make_patch(self) -> Self:
        self._factory.patch = misc.Patch.make(self._factory)
        return self

    def make_fx(self) -> Self:
        self._factory.fx = misc.FX(self._factory)
        return self


class FactoryBase(Remote):
    """Base class for factories, subclasses Remote."""

    def __init__(self, kind_id: str, **kwargs):
        defaultevents = {"pdirty": True, "mdirty": True, "midi": True, "ldirty": False}
        if "subs" in kwargs:
            defaultevents = defaultevents | kwargs.pop("subs")
        defaultkwargs = {"sync": False, "ratelimit": 0.033, "subs": defaultevents}
        kwargs = defaultkwargs | kwargs
        self.kind = kindmap(kind_id)
        super().__init__(**kwargs)
        self.builder = FactoryBuilder(self, self.kind)
        self._steps = (
            self.builder.make_strip,
            self.builder.make_bus,
            self.builder.make_command,
            self.builder.make_macrobutton,
            self.builder.make_vban,
            self.builder.make_device,
            self.builder.make_option,
        )
        self._configs = None

    def __str__(self) -> str:
        return f"Voicemeeter {self.kind}"

    @property
    @abstractmethod
    def steps(self):
        pass

    @cached_property
    def configs(self):
        self._configs = configs(self.kind.name)
        return self._configs


class BasicFactory(FactoryBase):
    """
    Represents a Basic Remote subclass

    Responsible for directing the builder class
    """

    def __new__(cls, *args, **kwargs):
        if cls is BasicFactory:
            raise TypeError(f"'{cls.__name__}' does not support direct instantiation")
        return object.__new__(cls)

    def __init__(self, kind_id, **kwargs):
        super().__init__(kind_id, **kwargs)
        [step()._pinfo(step.__name__) for step in self.steps]

    @property
    def steps(self) -> Iterable:
        """steps required to build the interface for a kind"""
        return self._steps


class BananaFactory(FactoryBase):
    """
    Represents a Banana Remote subclass

    Responsible for directing the builder class
    """

    def __new__(cls, *args, **kwargs):
        if cls is BananaFactory:
            raise TypeError(f"'{cls.__name__}' does not support direct instantiation")
        return object.__new__(cls)

    def __init__(self, kind_id, **kwargs):
        super().__init__(kind_id, **kwargs)
        [step()._pinfo(step.__name__) for step in self.steps]

    @property
    def steps(self) -> Iterable:
        """steps required to build the interface for a kind"""
        return self._steps + (self.builder.make_recorder, self.builder.make_patch)


class PotatoFactory(FactoryBase):
    """
    Represents a Potato Remote subclass

    Responsible for directing the builder class
    """

    def __new__(cls, *args, **kwargs):
        if cls is PotatoFactory:
            raise TypeError(f"'{cls.__name__}' does not support direct instantiation")
        return object.__new__(cls)

    def __init__(self, kind_id: str, **kwargs):
        super().__init__(kind_id, **kwargs)
        [step()._pinfo(step.__name__) for step in self.steps]

    @property
    def steps(self) -> Iterable:
        """steps required to build the interface for a kind"""
        return self._steps + (
            self.builder.make_recorder,
            self.builder.make_patch,
            self.builder.make_fx,
        )


def remote_factory(kind_id: str, **kwargs) -> Remote:
    """
    Factory method, invokes a factory creation class of a kind

    Returns a Remote class of a kind
    """
    match kind_id:
        case "basic":
            _factory = BasicFactory
        case "banana":
            _factory = BananaFactory
        case "potato":
            _factory = PotatoFactory
        case _:
            raise ValueError(f"Unknown Voicemeeter kind '{kind_id}'")
    return type(f"Remote{kind_id.capitalize()}", (_factory,), {})(kind_id, **kwargs)


def request_remote_obj(kind_id: str, **kwargs) -> Remote:
    """
    Interface entry point. Wraps factory method and handles errors

    Returns a reference to a Remote class of a kind
    """
    REMOTE_obj = None
    try:
        REMOTE_obj = remote_factory(kind_id, **kwargs)
    except (ValueError, TypeError) as e:
        raise SystemExit(e)
    return REMOTE_obj
