import logging

import voicemeeterlib

logging.basicConfig(level=logging.INFO)


class Observer:
    def __init__(self, vm):
        self.vm = vm
        # register your app as event observer
        self.vm.subject.add(self)
        # enable level updates, since they are disabled by default.
        self.vm.event.ldirty = True

    # define an 'on_update' callback function to receive event updates
    def on_update(self, subject):
        if subject == "pdirty":
            print("pdirty!")
        elif subject == "mdirty":
            print("mdirty!")
        elif subject == "ldirty":
            for bus in self.vm.bus:
                if bus.levels.isdirty:
                    print(bus, bus.levels.all)
        elif subject == "midi":
            current = self.vm.midi.current
            print(f"Value of midi button {current} is {self.vm.midi.get(current)}")


def main():
    kind_id = "banana"

    with voicemeeterlib.api(kind_id) as vm:
        Observer(vm)

        while cmd := input("Press <Enter> to exit\n"):
            if not cmd:
                break


if __name__ == "__main__":
    main()
