import json
import logging
import time
from logging import config

import voicemeeterlib

logging.basicConfig(level=logging.INFO)


class App:
    def __init__(self, vm):
        self.vm = vm
        # register the callbacks for each event
        self.vm.observer.add(
            [self.on_pdirty, self.on_mdirty, self.on_ldirty, self.on_midi]
        )

    def __enter__(self):
        self.vm.init_thread()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.vm.end_thread()

    def on_pdirty(self):
        print("pdirty!")

    def on_mdirty(self):
        print("mdirty!")

    def on_ldirty(self):
        for bus in self.vm.bus:
            if bus.levels.isdirty:
                print(bus, bus.levels.all)

    def on_midi(self):
        current = self.vm.midi.current
        print(f"Value of midi button {current} is {self.vm.midi.get(current)}")


def main():
    KIND_ID = "banana"

    with voicemeeterlib.api(KIND_ID) as vm:
        with App(vm) as app:
            for i in range(5, 0, -1):
                print(f"events start in {i} seconds")
                time.sleep(1)
            vm.event.add(["pdirty", "ldirty", "midi", "mdirty"])
            time.sleep(30)


if __name__ == "__main__":
    main()
