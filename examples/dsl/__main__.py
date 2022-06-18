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
        self.kls = Group(OneOrMore(Word(alphanums)))
        self.token = Suppress("->")
        self.param = Word(alphanums)
        self.value = Combine(
            Optional("-") + Word(nums) + Optional(".") + Optional(Word(nums))
        ) | Group(OneOrMore(Word(alphanums)))

    def parse(self, cmds):
        event = (
            self.kls
            + self.token
            + self.param
            + Optional(self.token)
            + Optional(self.value)
        )
        res = list()

        for cmd in cmds:
            if len(event.parseString(cmd)) == 2:
                kls, param = event.parseString(cmd)
                target = getattr(self.vm, kls[0])[int(kls[-1])]
                res.append(getattr(target, param))
            elif len(event.parseString(cmd)) == 3:
                kls, param, val = event.parseString(cmd)
                target = getattr(self.vm, kls[0])[int(kls[-1])]
                if "".join(val) in ["off", "on"]:
                    setattr(target, param, bool(["off", "on"].index("".join(val))))
                elif param in ["gain", "comp", "gate", "limit", "audibility"]:
                    setattr(target, param, float("".join(val)))
                elif param in ["label"]:
                    setattr(target, param, " ".join(val))

            time.sleep(0.05)
        return res


def main(cmds=None):
    kind_id = "banana"

    with voicemeeterlib.api(kind_id) as vm:
        parser = Parser(vm)
        if cmds:
            res = parser.parse(cmds)
            if res:
                print(res)
        else:
            try:
                while True:
                    cmd = input("please enter command (Return to exit)\n")
                    if not cmd:
                        break
                    res = parser.parse((cmd,))
                    if res:
                        print(res)
            except KeyboardInterrupt as e:
                SystemExit(e)


if __name__ == "__main__":
    cmds = (
        "strip 0 -> mute -> on",
        "strip 0 -> mute",
        "bus 0 -> mute -> on",
        "strip 0 -> mute -> off",
        "bus 0 -> mute -> on",
        "strip 3 -> solo -> on",
        "strip 3 -> solo -> off",
        "strip 1 -> A1 -> on",
        "strip 1 -> A1",
        "strip 1 -> A1 -> off",
        "strip 1 -> A1",
        "bus 3 -> eq -> on",
        "bus 3 -> eq -> off",
        "strip 4 -> gain -> 1.2",
        "strip 0 -> gain -> -8.2",
        "strip 0 -> gain",
        "strip 1 -> label -> rode podmic",
        "strip 2 -> limit -> -28",
        "strip 2 -> limit",
    )

    # pass cmds to parse cmds, otherwise simply run main() to test stdin parsing
    main(cmds)
