import time
from logging import config

import obsws_python as obsws

import voicemeeterlib

config.dictConfig(
    {
        "version": 1,
        "formatters": {
            "standard": {
                "format": "%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s"
            }
        },
        "handlers": {
            "stream": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "standard",
            }
        },
        "loggers": {
            "voicemeeterlib.iremote": {"handlers": ["stream"], "level": "DEBUG"}
        },
    }
)


class MyClient:
    def __init__(self, vm):
        self.vm = vm
        self.client = obsws.EventClient()
        self.client.callback.register(
            (
                self.on_current_program_scene_changed,
                self.on_exit_started,
            )
        )
        self.is_running = True

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
                "strip-0": {"mute": True, "comp": {"ratio": 4.3}},
                "strip-1": {"mute": True, "B1": False, "gate": {"attack": 2.3}},
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

    def on_exit_started(self, _):
        self.client.unsubscribe()
        self.is_running = False


def main():
    KIND_ID = "potato"

    with voicemeeterlib.api(KIND_ID) as vm:
        client = MyClient(vm)
        while client.is_running:
            time.sleep(0.1)


if __name__ == "__main__":
    main()
