import logging

import voicemeeterlib

logging.basicConfig(level=logging.INFO)


class Observer:
    # leftmost M on korg nanokontrol2 in CC mode
    MIDI_BUTTON = 48
    MACROBUTTON = 0

    def __init__(self, vm):
        self.vm = vm
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

        checks if midi button 48 velocity is 127 (full velocity for button press).
        """
        if (
            max(self.vm.strip[3].levels.postfader) > -40
            and self.vm.midi.get(self.MIDI_BUTTON) == 127
        ):
            print(
                f"Strip 3 level is greater than -40 and midi button {self.MIDI_BUTTON} is pressed"
            )
            self.vm.button[self.MACROBUTTON].trigger = True
        else:
            self.vm.button[self.MACROBUTTON].trigger = False
            self.vm.button[self.MACROBUTTON].state = False


def main():
    kind_id = "banana"

    # we only care about midi events here.
    subs = {ev: False for ev in ["pdirty", "mdirty"]}
    with voicemeeterlib.api(kind_id, subs=subs) as vm:
        obs = Observer(vm)

        while cmd := input("Press <Enter> to exit\n"):
            if not cmd:
                break


if __name__ == "__main__":
    main()
