[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/onyx-and-iris/voicemeeter-api-python/blob/dev/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
![Tests Status](./tests/basic.svg?dummy=8484744)
![Tests Status](./tests/banana.svg?dummy=8484744)
![Tests Status](./tests/potato.svg?dummy=8484744)

# Python Wrapper for Voicemeeter API

This package offers a Python interface for the Voicemeeter Remote C API.

For an outline of past/future changes refer to: [CHANGELOG](CHANGELOG.md)

## Tested against

-   Basic 1.0.8.2
-   Banana 2.0.6.2
-   Potato 3.0.2.2

## Requirements

-   [Voicemeeter](https://voicemeeter.com/)
-   Python 3.11 or greater

## Installation

### `Pip`

Install voicemeeter-api package from your console

`pip install voicemeeter-api`

## `Use`

Simplest use case, use a context manager to request a Remote class of a kind.

Login and logout are handled for you in this scenario.

#### `__main__.py`

```python
import voicemeeterlib


class ManyThings:
    def __init__(self, vm):
        self.vm = vm

    def things(self):
        self.vm.strip[0].label = "podmic"
        self.vm.strip[0].mute = True
        print(
            f"strip 0 ({self.vm.strip[0].label}) has been set to {self.vm.strip[0].mute}"
        )

    def other_things(self):
        info = (
            f"bus 3 gain has been set to {self.vm.bus[3].gain}",
            f"bus 4 eq has been set to {self.vm.bus[4].eq}",
        )
        self.vm.bus[3].gain = -6.3
        self.vm.bus[4].eq = True
        print("\n".join(info))


def main():
    with voicemeeterlib.api(kind_id) as vm:
        do = ManyThings(vm)
        do.things()
        do.other_things()

        # set many parameters at once
        vm.apply(
            {
                "strip-2": {"A1": True, "B1": True, "gain": -6.0},
                "bus-2": {"mute": True},
                "button-0": {"state": True},
                "vban-in-0": {"on": True},
                "vban-out-1": {"name": "streamname"},
            }
        )


if __name__ == "__main__":
    kind_id = "banana"

    main()
```

Otherwise you must remember to call `vm.login()`, `vm.logout()` at the start/end of your code.

## `kind_id`

Pass the kind of Voicemeeter as an argument. kind_id may be:

-   `basic`
-   `banana`
-   `potato`

## `Available commands`

### Channels (strip/bus)

The following properties exist for audio channels.

-   `mono`: boolean
-   `mute`: boolean
-   `gain`: float, from -60 to 12
-   `mc`, `k`: boolean
-   `comp`, `gate`: float, from 0 to 10
-   `limit`: int, from -40 to 12
-   `A1 - A5`, `B1 - B3`: boolean
-   `eq`: boolean
-   `label`: string
-   `device`: string
-   `sr`: int

example:

```python
vm.strip[3].gain = 3.7
print(strip[0].label)

vm.bus[4].mono = true
```

### Macrobuttons

Three modes defined: state, stateonly and trigger.

-   `state`: boolean
-   `stateonly`: boolean
-   `trigger`: boolean

example:

```python
vm.button[37].state = true
vm.button[55].trigger = false
```

### Recorder

The following methods are Available

-   `play()`
-   `stop()`
-   `pause()`
-   `record()`
-   `ff()`
-   `rew()`
    The following properties accept boolean values.
-   `loop`: boolean
-   `A1 - A5`: boolean
-   `B1 - A3`: boolean
    Load accepts a string:
-   `load`: string

example:

```python
vm.recorder.play()
vm.recorder.stop()

# Enable loop play
vm.recorder.loop = True

# Disable recorder out channel B2
vm.recorder.B2 = False

# filepath as raw string
vm.recorder.load(r'C:\music\mytune.mp3')
```

### VBAN

-   `vm.vban.enable()` `vm.vban.disable()` Turn VBAN on or off

For each vban in/out stream the following properties are defined:

-   `on`: boolean
-   `name`: string
-   `ip`: string
-   `port`: int, range from 1024 to 65535
-   `sr`: int, (11025, 16000, 22050, 24000, 32000, 44100, 48000, 64000, 88200, 96000)
-   `channel`: int, from 1 to 8
-   `bit`: int, 16 or 24
-   `quality`: int, from 0 to 4
-   `route`: int, from 0 to 8

SR, channel and bit are defined as readonly for instreams. Attempting to write to those parameters will throw an error. They are read and write for outstreams.

example:

```python
# turn VBAN on
vm.vban.enable()

# turn on vban instream 0
vm.vban.instream[0].on = True

# set bit property for outstream 3 to 24
vm.vban.outstream[3].bit = 24
```

### Command

Certain 'special' commands are defined by the API as performing actions rather than setting values. The following methods are available:

-   `show()` : Bring Voiceemeter GUI to the front
-   `shutdown()` : Shuts down the GUI
-   `restart()` : Restart the audio engine

The following properties are write only and accept boolean values.

-   `showvbanchat`: boolean
-   `lock`: boolean

example:

```python
vm.command.restart()
vm.command.showvbanchat = true
```

### Multiple parameters

-   `apply`
    Set many strip/bus/macrobutton/vban parameters at once, for example:

```python
vm.apply(
    {
        "strip-2": {"A1": True, "B1": True, "gain": -6.0},
        "bus-2": {"mute": True},
        "button-0": {"state": True},
        "vban-in-0": {"on": True},
        "vban-out-1": {"name": "streamname"},
    }
)
```

Or for each class you may do:

```python
vm.strip[0].apply(mute: true, gain: 3.2, A1: true)
vm.vban.outstream[0].apply(on: true, name: 'streamname', bit: 24)
```

## Config Files

`vm.apply_config(<configname>)`

You may load config files in TOML format.
Three example profiles have been included with the package. Remember to save
current settings before loading a profile. To set one you may do:

```python
import voicemeeterlib
with voicemeeterlib.api('banana') as vm:
    vm.apply_config('example')
```

will load a config file at configs/banana/example.toml for Voicemeeter Banana.

## `Base Module`

### Remote class

Access to lower level Getters and Setters are provided with these functions:

-   `vm.get(param, is_string=false)`: For getting the value of any parameter. Set string to true if getting a property value expected to return a string.
-   `vm.set(param, value)`: For setting the value of any parameter.

Access to lower level polling functions are provided with these functions:

-   `vm.pdirty()`: Returns true if a parameter has been updated.
-   `vm.mdirty()`: Returns true if a macrobutton has been updated.
-   `vm.ldirty()`: Returns true if a level has been updated.

example:

```python
vm.get('Strip[2].Mute')
vm.set('Strip[4].Label', 'stripname')
vm.set('Strip[0].Gain', -3.6)
```

### Run tests

To run all tests:

```
pytest -v
```

### Official Documentation

-   [Voicemeeter Remote C API](https://github.com/onyx-and-iris/Voicemeeter-SDK/blob/main/VoicemeeterRemoteAPI.pdf)
