import logging

import voicemeeterlib

logging.basicConfig(level=logging.DEBUG)


class App:
    MIDI_BUTTON = 48  # leftmost M on korg nanokontrol2 in CC mode
    MACROBUTTON = 0

    def __init__(self, vm):
        self._vm = vm
        self._vm.observer.add(self.on_midi)

    def on_midi(self):
        if self.get_info() == self.MIDI_BUTTON:
            self.on_midi_press()

    def get_info(self):
        current = self._vm.midi.current
        print(f'Value of midi button {current} is {self._vm.midi.get(current)}')
        return current

    def on_midi_press(self):
        """if midi button 48 is pressed and strip 3 level max > -40, then set trigger for macrobutton 0"""

        if (
            self._vm.midi.get(self.MIDI_BUTTON) == 127
            and max(self._vm.strip[3].levels.postfader) > -40
        ):
            print(
                f'Strip 3 level max is greater than -40 and midi button {self.MIDI_BUTTON} is pressed'
            )
            self._vm.button[self.MACROBUTTON].trigger = True
        else:
            self._vm.button[self.MACROBUTTON].trigger = False


def main():
    KIND_ID = 'banana'

    with voicemeeterlib.api(KIND_ID, midi=True) as vm:
        App(vm)

        while _ := input('Press <Enter> to exit\n'):
            pass


if __name__ == '__main__':
    main()
