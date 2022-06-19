class Subject:
    """Adds support for observers"""

    def __init__(self):
        """list of current observers"""

        self._observers = list()

    @property
    def observers(self) -> list:
        """returns the current observers"""

        return self._observers

    def notify(self, modifier=None):
        """run callbacks on update"""

        [o.on_update(modifier) for o in self._observers]

    def add(self, observer):
        """adds an observer to _observers"""

        if observer not in self._observers:
            self._observers.append(observer)
        else:
            print(f"Failed to add: {observer}")

    def remove(self, observer):
        """removes an observer from _observers"""

        try:
            self._observers.remove(observer)
        except ValueError:
            print(f"Failed to remove: {observer}")

    def clear(self):
        """clears the _observers list"""

        self._observers.clear()
