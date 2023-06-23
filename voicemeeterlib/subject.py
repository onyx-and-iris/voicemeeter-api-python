import logging

logger = logging.getLogger(__name__)


class Subject:
    def __init__(self):
        """Adds support for observers and callbacks"""

        self._observers = list()
        self.logger = logger.getChild(self.__class__.__name__)

    @property
    def observers(self) -> list:
        """returns the current observers"""

        return self._observers

    def notify(self, event):
        """run callbacks on update"""

        for o in self._observers:
            if hasattr(o, "on_update"):
                o.on_update(event)
            else:
                if o.__name__ == f"on_{event}":
                    o()

    def add(self, observer):
        """adds an observer to observers"""

        try:
            iterator = iter(observer)
            for o in iterator:
                if o not in self._observers:
                    self._observers.append(o)
                    self.logger.info(f"{o} added to event observers")
                else:
                    self.logger.error(f"Failed to add {o} to event observers")
        except TypeError:
            if observer not in self._observers:
                self._observers.append(observer)
                self.logger.info(f"{observer} added to event observers")
            else:
                self.logger.error(f"Failed to add {observer} to event observers")

    register = add

    def remove(self, observer):
        """removes an observer from observers"""

        try:
            iterator = iter(observer)
            for o in iterator:
                try:
                    self._observers.remove(o)
                    self.logger.info(f"{o} removed from event observers")
                except ValueError:
                    self.logger.error(f"Failed to remove {o} from event observers")
        except TypeError:
            try:
                self._observers.remove(observer)
                self.logger.info(f"{observer} removed from event observers")
            except ValueError:
                self.logger.error(f"Failed to remove {observer} from event observers")

    deregister = remove

    def clear(self):
        """clears the observers list"""

        self._observers.clear()
