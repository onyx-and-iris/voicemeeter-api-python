import logging


class Event:
    """Keeps track of event subscriptions"""

    logger = logging.getLogger("event.event")

    def __init__(self, subs: dict):
        self.subs = subs

    def info(self, msg=None):
        info = (f"{msg} events",) if msg else ()
        if self.any():
            info += (f"now listening for {', '.join(self.get())} events",)
        else:
            info += (f"not listening for any events",)
        self.logger.info(", ".join(info))

    @property
    def pdirty(self):
        return self.subs["pdirty"]

    @property
    def mdirty(self):
        return self.subs["mdirty"]

    @property
    def midi(self):
        return self.subs["midi"]

    @property
    def ldirty(self):
        return self.subs["ldirty"]

    def get(self) -> list:
        return [k for k, v in self.subs.items() if v]

    def any(self) -> bool:
        return any(self.subs.values())

    def add(self, event):
        self.subs[event] = True
        self.info(f"{event} added to")

    def remove(self, event):
        self.subs[event] = False
        self.info(f"{event} removed from")
