import logging

import voicemeeterlib

logging.basicConfig(level=logging.INFO)


class App:
    def __init__(self, vm):
        self.vm = vm
        # register your app as event observer
        self.vm.observer.add(self)

    def __str__(self):
        return type(self).__name__

    # define an 'on_update' callback function to receive event updates
    def on_update(self, event):
        if event == "pdirty":
            print("pdirty!")
        elif event == "mdirty":
            print("mdirty!")
        elif event == "ldirty":
            for bus in self.vm.bus:
                if bus.levels.isdirty:
                    print(bus, bus.levels.all)
        elif event == "midi":
            current = self.vm.midi.current
            print(f"Value of midi button {current} is {self.vm.midi.get(current)}")


def main():
    KIND_ID = "banana"

    with voicemeeterlib.api(
        KIND_ID, **{k: True for k in ("pdirty", "mdirty", "ldirty", "midi")}
    ) as vm:
        App(vm)

        while cmd := input("Press <Enter> to exit\n"):
            pass


if __name__ == "__main__":
    main()
