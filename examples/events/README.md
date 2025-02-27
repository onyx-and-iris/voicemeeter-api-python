# Events

If you want to receive updates on certain events there are two routes you can take:

-   Register a class that implements an `on_update(self, event) -> None` method on the `{Remote}.subject` class.
-   Register callback functions/methods on the `{Remote}.subject` class, one for each type of update.

Included are examples of both approaches.
