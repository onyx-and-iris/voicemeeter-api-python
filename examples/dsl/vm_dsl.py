import time

import voicemeeterlib
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


class Parser:
    def __init__(self, vm):
        self.vm = vm
        self.kls = Word(alphas)
        self.token = Suppress("->")
        self.index = Word(nums)
        self.action = Word(alphanums)

    def parse(self, cmds):
        event = (
            self.kls
            + self.token
            + self.index
            + self.token
            + self.action
            + Optional(
                Combine(
                    Optional("-") + Word(nums) + Optional(".") + Optional(Word(nums))
                )
            )
            + Optional(self.action)
            + Optional(self.token)
            + Optional(Group(OneOrMore(Word(alphanums))))
        )

        for cmd in cmds:
            kls, index, param, val = event.parseString(cmd)
            kls = "".join(kls)
            index = int(*index)
            target = getattr(self.vm, kls)[index]
            if val in ["on", "off"]:
                setattr(target, param, 1 if val == "on" else 0)
            if param in ["gain", "comp", "gate", "limit", "audibility"]:
                setattr(target, param, float(val))
            if param in ["label"]:
                val = " ".join(val)
                setattr(target, param, val)

            time.sleep(0.05)


def main(cmds=None):
    with voicemeeterlib.api("banana") as vm:
        parser = Parser(vm)
        if cmds:
            parser.parse(cmds)
        else:
            try:
                while True:
                    cmd = input("please enter command (Return to exit)\n")
                    if not cmd:
                        break
                    parser.parse((cmd,))
            except KeyboardInterrupt as e:
                SystemExit(e)


if __name__ == "__main__":
    cmds = (
        "strip -> 0 -> mute on",
        "bus -> 0 -> mute on",
        "strip -> 0 -> mute off",
        "bus -> 0 -> mute on",
        "strip -> 3 -> solo on",
        "strip -> 3 -> solo off",
        "strip -> 1 -> A1 on",
        "strip -> 1 -> A1 off",
        "bus -> 3 -> eq on",
        "bus -> 3 -> eq off",
        "strip -> 4 -> gain 1.2",
        "strip -> 0 -> gain -8.2",
        "strip -> 1 -> label -> rode podmic",
        "strip -> 2 -> limit -28",
    )

    # pass cmds to parse cmds, otherwise simply run main() to test stdin parsing
    main(cmds)
