import obsstudio_sdk as obs
import voicemeeterlib


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


def on_current_program_scene_changed(data):
    scene = data.scene_name
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


if __name__ == "__main__":
    with voicemeeterlib.api("potato") as vm:
        cl = obs.EventClient()
        cl.callback.register(on_current_program_scene_changed)

        while cmd := input("<Enter> to exit\n"):
            if not cmd:
                break
