import logging
import threading
import time

from .util import comp

logger = logging.getLogger(__name__)


class Producer(threading.Thread):
    """Continously send job queue to the Updater thread at a rate of self._remote.ratelimit."""

    def __init__(self, remote, queue):
        super().__init__(name="producer", daemon=True)
        self._remote = remote
        self.queue = queue
        self.logger = logger.getChild(self.__class__.__name__)

    def run(self):
        while self._remote.running:
            if self._remote.event.pdirty:
                self.queue.put("pdirty")
            if self._remote.event.mdirty:
                self.queue.put("mdirty")
            if self._remote.event.midi:
                self.queue.put("midi")
            if self._remote.event.ldirty:
                self.queue.put("ldirty")
            time.sleep(self._remote.ratelimit)
        self.logger.debug(f"terminating {self.name} thread")
        self.queue.put(None)


class Updater(threading.Thread):
    def __init__(self, remote, queue):
        super().__init__(name="updater", daemon=True)
        self._remote = remote
        self.queue = queue
        self._remote._strip_comp = [False] * (self._remote.kind.num_strip_levels)
        self._remote._bus_comp = [False] * (self._remote.kind.num_bus_levels)
        (
            self._remote.cache["strip_level"],
            self._remote.cache["bus_level"],
        ) = self._remote._get_levels()
        self.logger = logger.getChild(self.__class__.__name__)

    def _update_comps(self, strip_level, bus_level):
        self._remote._strip_comp, self._remote._bus_comp = (
            tuple(not x for x in comp(self._remote.cache["strip_level"], strip_level)),
            tuple(not x for x in comp(self._remote.cache["bus_level"], bus_level)),
        )

    def run(self):
        """
        Continously update observers of dirty states.

        Generate _strip_comp, _bus_comp and update level cache if ldirty.
        """
        while event := self.queue.get():
            if event == "pdirty" and self._remote.pdirty:
                self._remote.subject.notify(event)
            elif event == "mdirty" and self._remote.mdirty:
                self._remote.subject.notify(event)
            elif event == "midi" and self._remote.get_midi_message():
                self._remote.subject.notify(event)
            elif event == "ldirty" and self._remote.ldirty:
                self._update_comps(self._remote._strip_buf, self._remote._bus_buf)
                self._remote.cache["strip_level"] = self._remote._strip_buf
                self._remote.cache["bus_level"] = self._remote._bus_buf
                self._remote.subject.notify(event)
        self.logger.debug(f"terminating {self.name} thread")
