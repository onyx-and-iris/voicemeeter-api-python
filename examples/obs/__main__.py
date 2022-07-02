import logging
import sys

import voicemeeterlib

logging.basicConfig(level=logging.INFO)

sys.path.append("../")
from obswebsocket import events, obsws


def on_start():
    vm.strip[0].mute = True


def on_brb():
    vm.strip[7].fadeto(0, 500)


def on_end():
    vm.strip[0].mute = True


def on_live():
    vm.strip[0].mute = False
    vm.strip[7].fadeto(-6, 500)


def on_switch(message):
    scene = message.getSceneName()
    match scene:
        case "START":
            on_start()
        case "BRB":
            on_brb()
        case "END":
            on_end()
        case "LIVE":
            on_live()
        case _:
            pass


with voicemeeterlib.api("potato") as vm:
    with obsws() as ws:
        ws.register(on_switch, events.SwitchScenes)

        while cmd := input("Press <Enter> to exit\n"):
            if not cmd:
                break
