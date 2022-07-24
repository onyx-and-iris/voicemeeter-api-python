import voicemeeterlib


class Observer:
    def __init__(self, vm, midi_btn, macrobutton):
        self.vm = vm
        self.midi_btn = midi_btn
        self.macrobutton = macrobutton

    def register(self):
        self.vm.subject.add(self)

    def on_update(self, subject):
        if subject == "midi":
            self.get_info()
            self.on_midi_press()

    def get_info(self):
        current = self.vm.midi.current
        print(f"Value of midi button {current} is {self.vm.midi.get(current)}")

    def on_midi_press(self):
        if (
            max(self.vm.strip[3].levels.postfader) > -40
            and self.vm.midi.get(self.midi_btn) != 0
        ):
            print(
                f"Strip 3 level is greater than -40 and midi button {self.midi_btn} is pressed"
            )
            self.vm.button[self.macrobutton].trigger = True
        else:
            self.vm.button[self.macrobutton].trigger = False
            self.vm.button[self.macrobutton].state = False


def main():
    with voicemeeterlib.api(kind_id) as vm:
        obs = Observer(vm, midi_btn, macrobutton)
        obs.register()

        while cmd := input("Press <Enter> to exit\n"):
            if not cmd:
                break


if __name__ == "__main__":
    kind_id = "banana"
    # leftmost M on korg nanokontrol2 in CC mode
    midi_btn = 48
    macrobutton = 0

    main()
