import logging

import obsws_python as obs
import voicemeeterlib

logging.basicConfig(level=logging.INFO)


class Observer:
    def __init__(self, vm):
        self.vm = vm
        self.client = obs.EventClient()
        self.client.callback.register(self.on_current_program_scene_changed)

    def on_start(self):
        self.vm.strip[0].mute = True
        self.vm.strip[1].B1 = True
        self.vm.strip[2].B2 = True

    def on_brb(self):
        self.vm.strip[7].fadeto(0, 500)
        self.vm.bus[0].mute = True

    def on_end(self):
        self.vm.apply(
            {
                "strip-0": {"mute": True},
                "strip-1": {"mute": True, "B1": False},
                "strip-2": {"mute": True, "B1": False},
                "vban-in-0": {"on": False},
            }
        )

    def on_live(self):
        self.vm.strip[0].mute = False
        self.vm.strip[7].fadeto(-6, 500)
        self.vm.strip[7].A3 = True
        self.vm.vban.instream[0].on = True

    def on_current_program_scene_changed(self, data):
        def fget(scene):
            run = {
                "START": self.on_start,
                "BRB": self.on_brb,
                "END": self.on_end,
                "LIVE": self.on_live,
            }
            return run.get(scene)

        scene = data.scene_name
        print(f"Switched to scene {scene}")
        if fn := fget(scene):
            fn()


def main():
    subs = {ev: False for ev in ["pdirty", "mdirty", "midi"]}
    with voicemeeterlib.api("potato", subs=subs) as vm:
        obs = Observer(vm)
        while cmd := input("<Enter> to exit\n"):
            if not cmd:
                break


if __name__ == "__main__":
    main()
