## About

This script demonstrates how to interact with the event thread/event object. It also demonstrates how to register event specific callbacks.

By default the interface does not broadcast any events. So even though our callbacks are registered, and the event thread has been initiated, we won't receive updates.

After five seconds the event object is used to subscribe to all events for a total of thirty seconds.

Remember that events can also be unsubscribed to with `vm.event.remove()`. Callbacks can also be deregistered using vm.observer.remove().

The same can be done without a context manager:

```python
    vm = voicemeeterlib.api(KIND_ID)
    vm.login()
    vm.observer.add(on_midi)    # register an `on_midi` callback function
    vm.init_thread()
    vm.event.add("midi")    # in this case we only subscribe to midi events.
    ...
    vm.end_thread()
    vm.logout()
```

Once initialized, the event thread will continously run until end_thread() is called. Even if all events are unsubscribed to.

## Use

Simply run the script and trigger events and you should see the output after 5 seconds. To trigger events do the following:

-   change GUI parameters to trigger pdirty
-   press any macrobutton to trigger mdirty
-   play audio through any bus to trigger ldirty
-   any midi input to trigger midi
