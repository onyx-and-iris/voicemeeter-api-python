import argparse
import logging
import time
from abc import ABC, abstractmethod
from enum import IntEnum

from pyparsing import (
    Combine,
    Group,
    OneOrMore,
    Optional,
    Suppress,
    Word,
    alphanums,
    nums,
)

import voicemeeterlib

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


argparser = argparse.ArgumentParser(description="creates a basic dsl")
argparser.add_argument("-i", action="store_true")
args = argparser.parse_args()


ParamKinds = IntEnum(
    "ParamKinds",
    "bool float string",
)


class Strategy(ABC):
    def __init__(self, target, param, val):
        self.target = target
        self.param = param
        self.val = val

    @abstractmethod
    def run(self):
        pass


class BoolStrategy(Strategy):
    def run(self):
        setattr(self.target, self.param, self.strtobool(self.val))

    def strtobool(self, val):
        """Convert a string representation of truth to it's numeric form."""

        val = val.lower()
        if val in ("y", "yes", "t", "true", "on", "1"):
            return 1
        elif val in ("n", "no", "f", "false", "off", "0"):
            return 0
        else:
            raise ValueError("invalid truth value %r" % (val,))


class FloatStrategy(Strategy):
    def run(self):
        setattr(self.target, self.param, float(self.val))


class StringStrategy(Strategy):
    def run(self):
        setattr(self.target, self.param, " ".join(self.val))


class Context:
    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def run(self):
        self.strategy.run()


class Parser:
    IS_STRING = ("label",)

    def __init__(self, vm):
        self.logger = logger.getChild(self.__class__.__name__)
        self.vm = vm
        self.kls = Group(OneOrMore(Word(alphanums)))
        self.token = Suppress("->")
        self.param = Group(OneOrMore(Word(alphanums)))
        self.value = Combine(
            Optional("-") + Word(nums) + Optional(".") + Optional(Word(nums))
        ) | Group(OneOrMore(Word(alphanums)))
        self.event = (
            self.kls
            + self.token
            + self.param
            + Optional(self.token)
            + Optional(self.value)
        )

    def converter(self, cmds):
        """determines the kind of parameter from the parsed string"""

        res = list()
        for cmd in cmds:
            self.logger.debug(f"running command: {cmd}")
            match cmd_parsed := self.event.parseString(cmd):
                case [[kls, index], [param]]:
                    target = getattr(self.vm, kls)[int(index)]
                    res.append(getattr(target, param))
                case [[kls, index], [param], val] if param in self.IS_STRING:
                    target = getattr(self.vm, kls)[int(index)]
                    context = self._get_context(ParamKinds.string, target, param, val)
                    context.run()
                case [[kls, index], [param], [val] | val]:
                    target = getattr(self.vm, kls)[int(index)]
                    try:
                        context = self._get_context(ParamKinds.bool, target, param, val)
                        context.run()
                    except ValueError as e:
                        self.logger.error(f"{e}... switching to float strategy")
                        context.strategy = FloatStrategy(target, param, val)
                        context.run()
                case [
                    [kls, index],
                    [secondary, param],
                    [val] | val,
                ]:
                    primary = getattr(self.vm, kls)[int(index)]
                    target = getattr(primary, secondary)
                    try:
                        context = self._get_context(ParamKinds.bool, target, param, val)
                        context.run()
                    except ValueError as e:
                        self.logger.error(f"{e}... switching to float strategy")
                        context.strategy = FloatStrategy(target, param, val)
                        context.run()
                case _:
                    self.logger.error(
                        f"unable to determine the kind of parameter from {cmd_parsed}"
                    )
            time.sleep(0.05)
        return res

    def _get_context(self, kind, *args):
        """
        determines a strategy for a kind of parameter and passes it to the context.
        """

        match kind:
            case ParamKinds.bool:
                context = Context(BoolStrategy(*args))
            case ParamKinds.float:
                context = Context(FloatStrategy(*args))
            case ParamKinds.string:
                context = Context(StringStrategy(*args))
        return context


def interactive_mode(parser):
    while cmd := input("Please enter command (Press <Enter> to exit)\n"):
        if res := parser.parse((cmd,)):
            print(res)


def main():
    # fmt: off
    cmds = (
        "strip 0 -> mute -> true", "strip 0 -> mute", "bus 0 -> mute -> true",
        "strip 0 -> mute -> false", "bus 0 -> mute -> true", "strip 3 -> solo -> true",
        "strip 3 -> solo -> false", "strip 1 -> A1 -> true", "strip 1 -> A1",
        "strip 1 -> A1 -> false", "strip 1 -> A1", "strip 3 -> eq on -> true",
        "bus 3 -> eq on -> false", "strip 4 -> gain -> 1.2", "strip 0 -> gain -> -8.2",
        "strip 0 -> gain", "strip 1 -> label -> rode podmic", "strip 2 -> limit -> -28",
        "strip 2 -> limit", "strip 3 -> comp knob -> 3.8"
    )
    # fmt: on

    with voicemeeterlib.api("potato") as vm:
        parser = Parser(vm)
        if args.i:
            interactive_mode(parser)
            return

        if res := parser.converter(cmds):
            print(res)


if __name__ == "__main__":
    main()
