import logging
from typing import Iterable, Union

logger = logging.getLogger(__name__)


class Event:
    """Keeps track of event subscriptions"""

    def __init__(self, subs: dict):
        self.subs = subs
        self.logger = logger.getChild(self.__class__.__name__)

    def info(self, msg=None):
        info = (f"{msg} events",) if msg else ()
        if self.any():
            info += (f"now listening for {', '.join(self.get())} events",)
        else:
            info += ("not listening for any events",)
        self.logger.info(", ".join(info))

    @property
    def pdirty(self) -> bool:
        return self.subs["pdirty"]

    @pdirty.setter
    def pdirty(self, val: bool):
        self.subs["pdirty"] = val
        self.info(f"pdirty {'added to' if val else 'removed from'}")

    @property
    def mdirty(self) -> bool:
        return self.subs["mdirty"]

    @mdirty.setter
    def mdirty(self, val: bool):
        self.subs["mdirty"] = val
        self.info(f"mdirty {'added to' if val else 'removed from'}")

    @property
    def midi(self) -> bool:
        return self.subs["midi"]

    @midi.setter
    def midi(self, val: bool):
        self.subs["midi"] = val
        self.info(f"midi {'added to' if val else 'removed from'}")

    @property
    def ldirty(self) -> bool:
        return self.subs["ldirty"]

    @ldirty.setter
    def ldirty(self, val: bool):
        self.subs["ldirty"] = val
        self.info(f"ldirty {'added to' if val else 'removed from'}")

    def get(self) -> list:
        return [k for k, v in self.subs.items() if v]

    def any(self) -> bool:
        return any(self.subs.values())

    def add(self, events: Union[str, Iterable[str]]):
        if isinstance(events, str):
            events = [events]
        for event in events:
            setattr(self, event, True)

    def remove(self, events: Union[str, Iterable[str]]):
        if isinstance(events, str):
            events = [events]
        for event in events:
            setattr(self, event, False)
