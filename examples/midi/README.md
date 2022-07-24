## About/Requirements

A simple demonstration showing how to use a midi controller with this API.

This script was written for and tested with a Korg NanoKontrol2 configured in CC mode.

In order to run this example script you will need to have setup Voicemeeter with a midi device in Menu->Midi Mapping.

## Use

The script launches Voicemeeter Banana version and assumes that is the version being tested (if it was already launched)

`get_info()` responds to any midi button press or midi slider movement and prints its' CC number and most recent value.

`on_midi_press()` should enable trigger mode for macrobutton 0 if peak level value for strip 3 exceeds -40 and midi button 48 is pressed. On the NanoKontrol2 midi button 48 corresponds to the leftmost M button. You may need to disable any Keyboard Shortcut assignment first.

For a clear illustration of what may be done fill in some commands in `Request for Button ON / Trigger IN` and `Request for Button OFF / Trigger OUT`.

## Resources

If you want to know how to setup the NanoKontrol2 for CC mode check the following resources.

-   [Korg NanoKontrol2 Manual](https://www.korg.com/us/support/download/manual/0/159/1912/)
-   [CC Mode Info](https://i.korg.com/uploads/Support/nanoKONTROL2_PG_E1_634479709631760000.pdf)
