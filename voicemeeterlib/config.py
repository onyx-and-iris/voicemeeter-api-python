import itertools
from pathlib import Path

import tomllib

from .kinds import request_kind_map as kindmap


class TOMLStrBuilder:
    """builds a config profile, as a string, for the toml parser"""

    def __init__(self, kind):
        self.kind = kind
        self.higher = itertools.chain(
            [f"strip-{i}" for i in range(kind.num_strip)],
            [f"bus-{i}" for i in range(kind.num_bus)],
        )

    def init_config(self, profile=None):
        self.virt_strip_params = (
            [
                "mute = false",
                "mono = false",
                "solo = false",
                "gain = 0.0",
            ]
            + [f"A{i} = false" for i in range(1, self.kind.phys_out + 1)]
            + [f"B{i} = false" for i in range(1, self.kind.virt_out + 1)]
        )
        self.phys_strip_params = self.virt_strip_params + [
            "comp = 0.0",
            "gate = 0.0",
        ]
        self.bus_bool = ["mono = false", "eq = false", "mute = false"]

        if profile == "reset":
            self.reset_config()

    def reset_config(self):
        self.phys_strip_params = list(
            map(lambda x: x.replace("B1 = false", "B1 = true"), self.phys_strip_params)
        )
        self.virt_strip_params = list(
            map(lambda x: x.replace("A1 = false", "A1 = true"), self.virt_strip_params)
        )

    def build(self, profile="reset"):
        self.init_config(profile)
        toml_str = str()
        for eachclass in self.higher:
            toml_str += f"[{eachclass}]\n"
            toml_str = self.join(eachclass, toml_str)
        return toml_str

    def join(self, eachclass, toml_str):
        kls, index = eachclass.split("-")
        match kls:
            case "strip":
                toml_str += ("\n").join(
                    self.phys_strip_params
                    if int(index) < self.kind.phys_in
                    else self.virt_strip_params
                )
            case "bus":
                toml_str += ("\n").join(self.bus_bool)
            case _:
                pass
        return toml_str + "\n"


class TOMLDataExtractor:
    def __init__(self, file):
        self._data = dict()
        with open(file, "rb") as f:
            self._data = tomllib.load(f)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value


def dataextraction_factory(file):
    """
    factory function for parser

    this opens the possibility for other parsers to be added
    """
    if file.suffix == ".toml":
        extractor = TOMLDataExtractor
    else:
        raise ValueError("Cannot extract data from {}".format(file))
    return extractor(file)


class SingletonType(type):
    """ensure only a single instance of Loader object"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Loader(metaclass=SingletonType):
    """
    invokes the parser

    checks if config already in memory

    loads data into memory if not found
    """

    def __init__(self, kind):
        self._kind = kind
        self._configs = dict()
        self.defaults(kind)
        self.parser = None

    def defaults(self, kind):
        self.builder = TOMLStrBuilder(kind)
        toml_str = self.builder.build()
        self.register("reset", tomllib.loads(toml_str))

    def parse(self, identifier, data):
        if identifier in self._configs:
            print(f"config file with name {identifier} already in memory, skipping..")
            return False
        self.parser = dataextraction_factory(data)
        return True

    def register(self, identifier, data=None):
        self._configs[identifier] = data if data else self.parser.data
        print(f"config {self.name}/{identifier} loaded into memory")

    def deregister(self):
        self._configs.clear()
        self.defaults(self._kind)

    @property
    def configs(self):
        return self._configs

    @property
    def name(self):
        return self._kind.name


def loader(kind):
    """
    traverses defined paths for config files

    directs the loader

    returns configs loaded into memory
    """
    loader = Loader(kind)

    for path in (
        Path.cwd() / "configs" / kind.name,
        Path(__file__).parent / "configs" / kind.name,
        Path.home() / "Documents/Voicemeeter" / "configs" / kind.name,
    ):
        if path.is_dir():
            print(f"Checking [{path}] for TOML config files:")
            for file in path.glob("*.toml"):
                identifier = file.with_suffix("").stem
                if loader.parse(identifier, file):
                    loader.register(identifier)
    return loader.configs


def request_config(kind_id: str):
    """
    config entry point.

    Returns all configs loaded into memory for a kind
    """
    try:
        configs = loader(kindmap(kind_id))
    except KeyError as e:
        print(f"Unknown Voicemeeter kind '{kind_id}'")
    return configs
