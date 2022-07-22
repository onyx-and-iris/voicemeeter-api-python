import logging
import sys

import voicemeeterlib

logging.basicConfig(level=logging.INFO)

sys.path.append("../")
from obswebsocket import events, obsws


def on_start():
    vm.strip[0].mute = True
    vm.strip[1].B1 = True
    vm.strip[2].B2 = True


def on_brb():
    vm.strip[7].fadeto(0, 500)
    vm.bus[0].mute = True


def on_end():
    vm.apply(
        {
            "strip-0": {"mute": True},
            "strip-1": {"mute": True, "B1": False},
            "strip-2": {"mute": True, "B1": False},
            "vban-in-0": {"on": False},
        }
    )


def on_live():
    vm.strip[0].mute = False
    vm.strip[7].fadeto(-6, 500)
    vm.strip[7].A3 = True
    vm.vban.instream[0].on = True


def on_switch(message):
    scene = message.getSceneName()
    print(f"Switched to scene {scene}")

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
