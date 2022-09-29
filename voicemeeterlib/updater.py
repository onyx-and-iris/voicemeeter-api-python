import threading
import time

from .util import comp


class Updater(threading.Thread):
    def __init__(self, remote):
        super().__init__(name="updater", target=self.update, daemon=True)
        self._remote = remote

    def update(self):
        """
        Continously update observers of dirty states.

        Generate _strip_comp, _bus_comp and update level cache if ldirty.

        Runs updates at a rate of self.ratelimit.
        """
        while self._remote.running:
            start = time.time()
            if self._remote.event.pdirty and self._remote.pdirty:
                self._remote.subject.notify("pdirty")
            if self._remote.event.mdirty and self._remote.mdirty:
                self._remote.subject.notify("mdirty")
            if self._remote.event.midi and self._remote.get_midi_message():
                self._remote.subject.notify("midi")
            if self._remote.event.ldirty and self._remote.ldirty:
                self._remote._strip_comp, self._remote._bus_comp = (
                    tuple(
                        not x
                        for x in comp(
                            self._remote.cache["strip_level"], self._remote._strip_buf
                        )
                    ),
                    tuple(
                        not x
                        for x in comp(
                            self._remote.cache["bus_level"], self._remote._bus_buf
                        )
                    ),
                )
                self._remote.cache["strip_level"] = self._remote._strip_buf
                self._remote.cache["bus_level"] = self._remote._bus_buf
                self._remote.subject.notify("ldirty")

            elapsed = time.time() - start
            if self._remote.event.any() and self._remote.ratelimit - elapsed > 0:
                time.sleep(self._remote.ratelimit - elapsed)
            else:
                time.sleep(0.1)
