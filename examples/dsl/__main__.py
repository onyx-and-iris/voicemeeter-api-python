import argparse
import logging
import time

from pyparsing import (
    Combine,
    Group,
    OneOrMore,
    Optional,
    Suppress,
    Word,
    alphanums,
    alphas,
    nums,
)

import voicemeeterlib

logging.basicConfig(level=logging.INFO)
argparser = argparse.ArgumentParser(description="creates a basic dsl")
argparser.add_argument("-i", action="store_true")
args = argparser.parse_args()


class Parser:
    def __init__(self, vm):
        self.vm = vm
        self.kls = Group(OneOrMore(Word(alphanums)))
        self.token = Suppress("->")
        self.param = Word(alphanums)
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

    def parse(self, cmds):
        res = list()

        for cmd in cmds:
            if len(self.event.parseString(cmd)) == 2:
                kls, param = self.event.parseString(cmd)
                target = getattr(self.vm, kls[0])[int(kls[-1])]
                res.append(getattr(target, param))
            elif len(self.event.parseString(cmd)) == 3:
                kls, param, val = self.event.parseString(cmd)
                target = getattr(self.vm, kls[0])[int(kls[-1])]
                if "".join(val) in ["off", "on"]:
                    setattr(target, param, bool(["off", "on"].index("".join(val))))
                elif param in ["gain", "comp", "gate", "limit", "audibility"]:
                    setattr(target, param, float("".join(val)))
                elif param in ["label"]:
                    setattr(target, param, " ".join(val))

            time.sleep(0.05)
        return res


def interactive_mode(parser):
    while cmd := input("Please enter command (Press <Enter> to exit)\n"):
        if not cmd:
            break
        if res := parser.parse((cmd,)):
            print(res)


def main():
    # fmt: off
    cmds = (
        "strip 0 -> mute -> on", "strip 0 -> mute", "bus 0 -> mute -> on",
        "strip 0 -> mute -> off", "bus 0 -> mute -> on", "strip 3 -> solo -> on",
        "strip 3 -> solo -> off", "strip 1 -> A1 -> on", "strip 1 -> A1",
        "strip 1 -> A1 -> off", "strip 1 -> A1", "bus 3 -> eq -> on",
        "bus 3 -> eq -> off", "strip 4 -> gain -> 1.2", "strip 0 -> gain -> -8.2",
        "strip 0 -> gain", "strip 1 -> label -> rode podmic", "strip 2 -> limit -> -28",
        "strip 2 -> limit",
    )
    # fmt: on

    KIND_ID = "banana"

    with voicemeeterlib.api(KIND_ID) as vm:
        parser = Parser(vm)
        if args.i:
            interactive_mode(parser)
            return

        if res := parser.parse(cmds):
            print(res)


if __name__ == "__main__":
    main()
