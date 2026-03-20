import logging

logger = logging.getLogger(__name__)


class Subject:
    def __init__(self):
        """Adds support for observers and callbacks"""

        self._observers = []
        self.logger = logger.getChild(self.__class__.__name__)

    @property
    def observers(self) -> list:
        """returns the current observers"""

        return self._observers

    def notify(self, event):
        """run callbacks on update"""

        for o in self._observers:
            if hasattr(o, 'on_update'):
                o.on_update(event)
            else:
                if o.__name__ == f'on_{event}':
                    o()

    def add(self, observer):
        """adds an observer to observers"""

        try:
            iterator = iter(observer)
            for o in iterator:
                if o not in self._observers:
                    self._observers.append(o)
                else:
                    self.logger.debug(f'Observer {o} already in observers list')
        except TypeError:
            if observer not in self._observers:
                self._observers.append(observer)
            else:
                self.logger.debug(f'Observer {observer} already in observers list')

    register = add

    def remove(self, observer):
        """removes an observer from observers"""

        try:
            iterator = iter(observer)
            for o in iterator:
                try:
                    self._observers.remove(o)
                except ValueError:
                    self.logger.debug(f'Observer {o} not found in observers list')
        except TypeError:
            try:
                self._observers.remove(observer)
            except ValueError:
                self.logger.debug(f'Observer {observer} not found in observers list')

    deregister = remove

    def clear(self):
        """clears the observers list"""

        self._observers.clear()
