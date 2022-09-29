import logging

import voicemeeterlib


class Observer:
    def __init__(self, vm):
        self.vm = vm
        # register your app as event observer
        self.vm.subject.add(self)
        # add level updates, since they are disabled by default.
        self.vm.event.add("ldirty")

    # define an 'on_update' callback function to receive event updates
    def on_update(self, subject):
        if subject == "pdirty":
            print("pdirty!")
        elif subject == "mdirty":
            print("mdirty!")
        elif subject == "ldirty":
            info = (
                f"[{self.vm.bus[0]} {self.vm.bus[0].levels.isdirty}]",
                f"[{self.vm.bus[1]} {self.vm.bus[1].levels.isdirty}]",
                f"[{self.vm.bus[2]} {self.vm.bus[2].levels.isdirty}]",
                f"[{self.vm.bus[3]} {self.vm.bus[3].levels.isdirty}]",
                f"[{self.vm.bus[4]} {self.vm.bus[4].levels.isdirty}]",
            )
            print(" ".join(info))
        elif subject == "midi":
            current = self.vm.midi.current
            print(f"Value of midi button {current} is {self.vm.midi.get(current)}")


def main():
    with voicemeeterlib.api(kind_id) as vm:
        Observer(vm)

        while cmd := input("Press <Enter> to exit\n"):
            if not cmd:
                break


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    kind_id = "banana"

    main()
