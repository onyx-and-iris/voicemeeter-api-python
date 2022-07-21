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

### Strip

The following properties are available.

-   `mono`: boolean
-   `solo`: boolean
-   `mute`: boolean
-   `gain`: float, from -60.0 to 12.0
-   `comp`: float, from 0.0 to 10.0
-   `gate`: float, from 0.0 to 10.0
-   `audibility`: float, from 0.0 to 10.0
-   `limit`: int, from -40 to 12
-   `A1 - A5`, `B1 - B3`: boolean
-   `label`: string
-   `device`: string
-   `sr`: int
-   `mc`: boolean
-   `k`: int, from 0 to 4
-   `bass`: float, from -12.0 to 12.0
-   `mid`: float, from -12.0 to 12.0
-   `treble`: float, from -12.0 to 12.0
-   `reverb`: float, from 0.0 to 10.0
-   `delay`: float, from 0.0 to 10.0
-   `fx1`: float, from 0.0 to 10.0
-   `fx2`: float, from 0.0 to 10.0
-   `pan_x`: float, from -0.5 to 0.5
-   `pan_y`: float, from 0.0 to 1.0
-   `color_x`: float, from -0.5 to 0.5
-   `color_y`: float, from 0.0 to 1.0
-   `fx_x`: float, from -0.5 to 0.5
-   `fx_y`: float, from 0.0 to 1.0
-   `postreverb`: boolean
-   `postdelay`: boolean
-   `postfx1`: boolean
-   `postfx2`: boolean

example:

```python
vm.strip[3].gain = 3.7
print(vm.strip[0].label)
```

The following methods are Available.

-   `appgain(name, value)`: string, float, from 0.0 to 1.0

Set the gain in db by value for the app matching name.

-   `appmute(name, value)`: string, bool

Set mute state as value for the app matching name.

example:

```python
vm.strip[5].appmute("Spotify", True)
vm.strip[5].appgain("Spotify", 0.5)
```

##### Gainlayers

-   `gain`: float, from -60.0 to 12.0

example:

```python
vm.strip[3].gainlayer[3].gain = 3.7
```

Gainlayers are defined for potato version only.

##### Levels

The following properties are available.

-   `prefader`
-   `postfader`
-   `postmute`

example:

```python
print(vm.strip[3].levels.prefader)
```

Level properties will return -200.0 if no audio detected.

### Bus

The following properties are available.

-   `mono`: boolean
-   `eq`: boolean
-   `eq_ab`: boolean
-   `mute`: boolean
-   `sel`: boolean
-   `gain`: float, from -60.0 to 12.0
-   `label`: string
-   `device`: string
-   `sr`: int
-   `returnreverb`: float, from 0.0 to 10.0
-   `returndelay`: float, from 0.0 to 10.0
-   `returnfx1`: float, from 0.0 to 10.0
-   `returnfx2`: float, from 0.0 to 10.0
-   `monitor`: boolean

example:

```python
vm.bus[3].gain = 3.7
print(vm.bus[0].label)

vm.bus[4].mono = True
```

##### Modes

The following properties are available.

-   `normal`: boolean
-   `amix`: boolean
-   `bmix`: boolean
-   `composite`: boolean
-   `tvmix`: boolean
-   `upmix21`: boolean
-   `upmix41`: boolean
-   `upmix61`: boolean
-   `centeronly`: boolean
-   `lfeonly`: boolean
-   `rearonly`: boolean

The following methods are available.

-   `get()`: Returns the current bus mode

example:

```python
vm.bus[4].mode.amix = True

print(vm.bus[2].mode.get())
```

##### Levels

The following properties are available.

-   `all`

example:

```python
print(vm.bus[0].levels.all)
```

`levels.all` will return -200.0 if no audio detected.

### Strip | Bus

The following methods are available.

-   `fadeto(amount, time)`: float, int
-   `fadeby(amount, time)`: float, int

Modify gain to or by the selected amount in db over a time interval in ms.

example:

```python
vm.strip[0].fadeto(-10.3, 1000)
vm.bus[3].fadeby(-5.6, 500)
```

### Macrobuttons

The following properties are available.

-   `state`: boolean
-   `stateonly`: boolean
-   `trigger`: boolean

example:

```python
vm.button[37].state = True
vm.button[55].trigger = False
```

### Recorder

The following methods are available

-   `play()`
-   `stop()`
-   `pause()`
-   `record()`
-   `ff()`
-   `rew()`
-   `load(<filepath>)`: string

The following properties are available

-   `loop`: boolean
-   `A1 - A5`: boolean
-   `B1 - A3`: boolean

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

Recorder properties are defined as write only.

### VBAN

-   `vm.vban.enable()` `vm.vban.disable()` Turn VBAN on or off

##### Instream | Outstream

The following properties are available.

-   `on`: boolean
-   `name`: string
-   `ip`: string
-   `port`: int, range from 1024 to 65535
-   `sr`: int, (11025, 16000, 22050, 24000, 32000, 44100, 48000, 64000, 88200, 96000)
-   `channel`: int, from 1 to 8
-   `bit`: int, 16 or 24
-   `quality`: int, from 0 to 4
-   `route`: int, from 0 to 8

`SR`, `channel` and `bit` are defined as:

-   readonly for instreams.
-   read and write for outstreams.

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

Certain 'special' commands are defined by the API as performing actions rather than setting values.

The following methods are available:

-   `show()` : Bring Voiceemeter GUI to the front
-   `shutdown()` : Shuts down the GUI
-   `restart()` : Restart the audio engine
-   `reset()`: Applies the `reset` config. (phys strip B1, virt strip A1, gains, comp, gate 0.0, mute, mono, solo, eq false)

The following properties are available.

-   `showvbanchat`: boolean
-   `lock`: boolean

example:

```python
vm.command.restart()
vm.command.showvbanchat = True
```

`showvbanchat` and `lock` are write only.

### Device

-   `ins` `outs` : Returns the number of input/output devices
-   `input(i)` `output(i)` : Returns a dict of device properties for device[i]

example:

```python
import voicemeeterlib
with voicemeeterlib.api(kind_id) as vm:
    for i in range(vm.device.ins):
        print(vm.device.input(i))
```

### FX

The following properties are available:

-   `reverb`: boolean
-   `reverb_ab`: boolean
-   `delay`: boolean
-   `delay_ab`: boolean

example:

```python
vm.fx.reverb_ab = True
```

### Patch

The following properties are available:

-   `postfadercomposite`: boolean
-   `postfxinsert`: boolean

example:

```python
vm.patch.postfxinsert = False
```

##### asio[i]

-   `get()`: int
-   `set(patch_in)`: int, valid range determined by connected device.

example:

```python
vm.patch.asio[3].set(4)
```

i, from 0 to 10

##### A2[i] - A5[i]

-   `get()`: int
-   `set(patch_out)`: int, valid range determined by connected device.

example:

```python
vm.patch.A3[5].set(18)
```

i, from 0 to 8.

##### composite[i]

-   `get()`: int
-   `set(channel)`: int, from 0 up to number of channels depending on version.

example:

```python
vm.patch.composite[7].set = 4
```

i, from 0 to 8.

##### insert[i]

-   `on`: boolean

example:

```python
vm.patch.insert[18].on = True
```

i, from 0 up to number of channels depending on version.

### Option

The following properties are available:

-   `sr`: int
-   `asiosr`: boolean
-   `monitoronsel`: boolean

example:

```python
vm.option.sr = 48000
```

The following methods are available:

-   `buffer(driver, buffer)` : Set buffer size for particular audio driver.

example:

```python
vm.option.buffer("wdm", 512)
```

driver defined as one of ("mme", "wdm", "ks", "asio")
buffer, from 128 to 2048

##### delay[i]

-   `get()`: int
-   `set(delay)`: int, from 0 to 500

example:

```python
vm.option.delay[4].set(30)
```

i, from 0 up to 4.

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
vm.strip[0].apply(mute: True, gain: 3.2, A1: True)
vm.vban.outstream[0].apply(on: True, name: 'streamname', bit: 24)
```

## Config Files

`vm.apply_config(<configname>)`

You may load config files in TOML format.
Three example configs have been included with the package. Remember to save
current settings before loading a user config. To set one you may do:

```python
import voicemeeterlib
with voicemeeterlib.api('banana') as vm:
    vm.apply_config('example')
```

will load a user config file at configs/banana/example.toml for Voicemeeter Banana.

## `Base Module`

### Remote class

Access to lower level Getters and Setters are provided with these functions:

-   `vm.get(param, is_string=False)`: For getting the value of any parameter. Set string to True if getting a property value expected to return a string.
-   `vm.set(param, value)`: For setting the value of any parameter.

Access to lower level polling functions are provided with these functions:

-   `vm.pdirty()`: Returns True if a parameter has been updated.
-   `vm.mdirty()`: Returns True if a macrobutton has been updated.
-   `vm.ldirty()`: Returns True if a level has been updated.

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
