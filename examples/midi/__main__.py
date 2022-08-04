import voicemeeterlib


class Observer:
    def __init__(self, vm, midi_btn, macrobutton):
        self.vm = vm
        self.midi_btn = midi_btn
        self.macrobutton = macrobutton

    def register(self):
        self.vm.subject.add(self)

    def on_update(self, subject):
        """
        We expect to only receive midi updates.

        We could skip subject check but check anyway, in case an event is added later.
        """
        if subject == "midi":
            self.get_info()
            self.on_midi_press()

    def get_info(self):
        current = self.vm.midi.current
        print(f"Value of midi button {current} is {self.vm.midi.get(current)}")

    def on_midi_press(self):
        """
        checks if strip 3 level postfader mode is greater than -40

        checks if midi button 48 velcity is 127 (full velocity for button press).
        """
        if (
            max(self.vm.strip[3].levels.postfader) > -40
            and self.vm.midi.get(self.midi_btn) == 127
        ):
            print(
                f"Strip 3 level is greater than -40 and midi button {self.midi_btn} is pressed"
            )
            self.vm.button[self.macrobutton].trigger = True
        else:
            self.vm.button[self.macrobutton].trigger = False
            self.vm.button[self.macrobutton].state = False


def main():
    # we only care about midi events here.
    subs = {ev: False for ev in ["pdirty", "mdirty", "ldirty"]}
    with voicemeeterlib.api(kind_id, subs=subs) as vm:
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
