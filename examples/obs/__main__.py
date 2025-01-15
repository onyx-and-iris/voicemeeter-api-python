import threading
from logging import config

import obsws_python as obsws

import voicemeeterlib

config.dictConfig(
    {
        'version': 1,
        'formatters': {
            'standard': {
                'format': '%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s'
            }
        },
        'handlers': {
            'stream': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            }
        },
        'loggers': {
            'voicemeeterlib.iremote': {'handlers': ['stream'], 'level': 'DEBUG'}
        },
    }
)


class MyClient:
    def __init__(self, vm, stop_event):
        self.vm = vm
        self._stop_event = stop_event
        self._client = obsws.EventClient()
        self._client.callback.register(
            (
                self.on_current_program_scene_changed,
                self.on_exit_started,
            )
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._client.disconnect()

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
                'strip-0': {'mute': True, 'comp': {'ratio': 4.3}},
                'strip-1': {'mute': True, 'B1': False, 'gate': {'attack': 2.3}},
                'strip-2': {'mute': True, 'B1': False},
                'vban-in-0': {'on': False},
            }
        )

    def on_live(self):
        self.vm.strip[0].mute = False
        self.vm.strip[7].fadeto(-6, 500)
        self.vm.strip[7].A3 = True
        self.vm.vban.instream[0].on = True

    def on_current_program_scene_changed(self, data):
        scene = data.scene_name
        print(f'Switched to scene {scene}')
        match scene:
            case 'START':
                self.on_start()
            case 'BRB':
                self.on_brb()
            case 'END':
                self.on_end()
            case 'LIVE':
                self.on_live()

    def on_exit_started(self, _):
        self._stop_event.set()


def main():
    KIND_ID = 'potato'

    with voicemeeterlib.api(KIND_ID) as vm:
        stop_event = threading.Event()

        with MyClient(vm, stop_event):
            stop_event.wait()


if __name__ == '__main__':
    main()
