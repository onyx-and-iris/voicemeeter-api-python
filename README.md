[![PyPI version](https://badge.fury.io/py/voicemeeter-api.svg)](https://badge.fury.io/py/voicemeeter-api)
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

-   Basic 1.0.8.8
-   Banana 2.0.6.8
-   Potato 3.0.2.8

## Requirements

-   [Voicemeeter](https://voicemeeter.com/)
-   Python 3.10 or greater

## Installation

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
            f"strip 0 ({self.vm.strip[0].label}) mute has been set to {self.vm.strip[0].mute}"
        )

    def other_things(self):
        self.vm.bus[3].gain = -6.3
        self.vm.bus[4].eq.on = True
        info = (
            f"bus 3 gain has been set to {self.vm.bus[3].gain}",
            f"bus 4 eq has been set to {self.vm.bus[4].eq.on}",
        )
        print("\n".join(info))


def main():
    KIND_ID = "banana"

    with voicemeeterlib.api(KIND_ID) as vm:
        do = ManyThings(vm)
        do.things()
        do.other_things()

        # set many parameters at once
        vm.apply(
            {
                "strip-2": {"A1": True, "B1": True, "gain": -6.0},
                "bus-2": {"mute": True, "eq": {"on": True}},
                "button-0": {"state": True},
                "vban-in-0": {"on": True},
                "vban-out-1": {"name": "streamname"},
            }
        )


if __name__ == "__main__":
    main()

```

Otherwise you must remember to call `vm.login()`, `vm.logout()` at the start/end of your code.

## `KIND_ID`

Pass the kind of Voicemeeter as an argument. KIND_ID may be:

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
-   `audibility`: float, from 0.0 to 10.0
-   `limit`: int, from -40 to 12
-   `A1 - A5`, `B1 - B3`: boolean
-   `label`: string
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

The following methods are available.

-   `appgain(name, value)`: string, float, from 0.0 to 1.0

Set the gain in db by value for the app matching name.

-   `appmute(name, value)`: string, bool

Set mute state as value for the app matching name.

example:

```python
vm.strip[5].appmute("Spotify", True)
vm.strip[5].appgain("Spotify", 0.5)
```

#### Strip.Comp

The following properties are available.

-   `knob`: float, from 0.0 to 10.0
-   `gainin`: float, from -24.0 to 24.0
-   `ratio`: float, from 1.0 to 8.0
-   `threshold`: float, from -40.0 to -3.0
-   `attack`: float, from 0.0 to 200.0
-   `release`: float, from 0.0 to 5000.0
-   `knee`: float, from 0.0 to 1.0
-   `gainout`: float, from -24.0 to 24.0
-   `makeup`: boolean

example:

```python
print(vm.strip[4].comp.knob)
```

Strip Comp parameters are defined for PhysicalStrips.

`knob` defined for all versions, all other parameters potato only.

#### Strip.Gate

The following properties are available.

-   `knob`: float, from 0.0 to 10.0
-   `threshold`: float, from -60.0 to -10.0
-   `damping`: float, from -60.0 to -10.0
-   `bpsidechain`: int, from 100 to 4000
-   `attack`: float, from 0.0 to 1000.0
-   `hold`: float, from 0.0 to 5000.0
-   `release`: float, from 0.0 to 5000.0

example:

```python
vm.strip[2].gate.attack = 300.8
```

Strip Gate parameters are defined for PhysicalStrips.

`knob` defined for all versions, all other parameters potato only.

#### Strip.Denoiser

The following properties are available.

-   `knob`: float, from 0.0 to 10.0

example:

```python
vm.strip[0].denoiser.knob = 0.5
```

Strip Denoiser parameters are defined for PhysicalStrips, potato version only.

#### Strip.EQ

The following properties are available.

-   `on`: boolean
-   `ab`: boolean

example:

```python
vm.strip[0].eq.ab = True
```

Strip EQ parameters are defined for PhysicalStrips, potato version only.

##### Strip.Gainlayers

-   `gain`: float, from -60.0 to 12.0

example:

```python
vm.strip[3].gainlayer[3].gain = 3.7
```

Gainlayers are defined for potato version only.

##### Strip.Levels

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
-   `mute`: boolean
-   `sel`: boolean
-   `gain`: float, from -60.0 to 12.0
-   `label`: string
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

##### Bus.EQ

The following properties are available.

-   `on`: boolean
-   `ab`: boolean

example:

```python
vm.bus[3].eq.on = True
```

##### Bus.Modes

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

##### Bus.Levels

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

#### Strip.Device | Bus.Device

The following properties are available

-   `name`: str
-   `sr`: int
-   `wdm`: str
-   `ks`: str
-   `mme`: str
-   `asio`: str

example:

```python
print(vm.strip[0].device.name)
vm.bus[0].device.asio = "Audient USB Audio ASIO Driver"
```

strip|bus device parameters are defined for physical channels only.

name, sr are read only. wdm, ks, mme, asio are write only.

### Macrobuttons

The following properties are available.

-   `state`: boolean
-   `stateonly`: boolean
-   `trigger`: boolean
-   `color`: int, from 0 to 8

example:

```python
vm.button[37].state = True
vm.button[4].color = 1
```

### Recorder

The following methods are available

-   `play()`
-   `stop()`
-   `pause()`
-   `record()`
-   `ff()`
-   `rew()`
-   `load(filepath)`: raw string
-   `goto(time_string)`: time string in format `hh:mm:ss`
-   `filetype(filetype)`: string, ("wav", "aiff", "bwf", "mp3")

The following properties are available

-   `A1 - A5`: boolean
-   `B1 - B3`: boolean
-   `samplerate`: int, (22050, 24000, 32000, 44100, 48000, 88200, 96000, 176400, 192000)
-   `bitresolution`: int, (8, 16, 24, 32)
-   `channel`: int, from 1 to 8
-   `kbps`: int, (32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320)
-   `gain`: float, from -60.0 to 12.0

example:

```python
vm.recorder.play()
vm.recorder.stop()

# Disable recorder out channel B2
vm.recorder.B2 = False

# filepath as raw string
vm.recorder.load(r'C:\music\mytune.mp3')

# set the goto time to 1m 30s
vm.recorder.goto("00:01:30")
```

#### Recorder.Mode

The following properties are available

-   `recbus`: boolean
-   `playonload`: boolean
-   `loop`: boolean
-   `multitrack`: boolean

example:

```python
# Enable loop play
vm.recorder.mode.loop = True
```

#### Recorder.ArmStrip[i]|ArmBus[i]

The following method is available

-   `set(val)`: boolean

example:

```python
# Arm strip 3
vm.recorder.armstrip[3].set(True)
# Arm bus 0
vm.recorder.armbus[0].set(True)
```

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
with voicemeeterlib.api(KIND_ID) as vm:
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
vm.patch.A3[5].set(3)
```

i, from 0 to 8.

##### composite[i]

-   `get()`: int
-   `set(channel)`: int, from 0 up to number of channels depending on version.

example:

```python
vm.patch.composite[7].set(4)
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

-   `buffer(driver, buf)` : Set buffer size for particular audio driver.
    -   buf: int, from 128 to 2048
    -   driver:str, ("mme", "wdm", "ks", "asio")

example:

```python
vm.option.buffer("wdm", 512)
```

##### delay[i]

-   `get()`: int
-   `set(delay)`: int, from 0 to 500

example:

```python
vm.option.delay[4].set(30)
```

i, from 0 up to 4.

### Midi

The following properties are available:

-   `channel`: int, returns the midi channel
-   `current`: int, returns the current (or most recently pressed) key

The following methods are available:

-   `get(key)`: int, returns most recent velocity value for a key

example:

```python
print(vm.midi.get(12))
```

get() may return None if no value for requested key in midi cache

### Multiple parameters

-   `apply`
    Set many strip/bus/macrobutton/vban parameters at once, for example:

```python
vm.apply(
    {
        "strip-2": {"A1": True, "B1": True, "gain": -6.0},
        "bus-2": {"mute": True, "eq": {"on": True}},
        "button-0": {"state": True},
        "vban-in-0": {"on": True},
        "vban-out-1": {"name": "streamname"},
    }
)
```

Or for each class you may do:

```python
vm.strip[0].apply({"mute": True, "gain": 3.2, "A1": True})
vm.vban.outstream[0].apply({"on": True, "name": "streamname", "bit": 24})
```

## Config Files

`vm.apply_config(configname)`

You may load config files in TOML format.
Three example configs have been included with the package. Remember to save
current settings before loading a user config. To load one you may do:

```python
import voicemeeterlib
with voicemeeterlib.api('banana') as vm:
    vm.apply_config('example')
```

Your configs may be located in one of the following paths:
-   \<current working directory\> / "configs" / kind_id
-   \<user home directory\> / ".config" / "voicemeeter" / kind_id
-   \<user home directory\> / "Documents" / "Voicemeeter" / "configs" / kind_id

If a config with the same name is located in multiple locations, only the first one found is loaded into memory, in the above order.

#### `config extends`

You may also load a config that extends another config with overrides or additional parameters.

You just need to define a key `extends` in the config TOML, that names the config to be extended.

Three example 'extender' configs are included with the repo. You may load them with:

```python
import voicemeeterlib
with voicemeeterlib.api('banana') as vm:
    vm.apply_config('extender')
```

## Events

By default, NO events are listened for. Use events kwargs to enable specific event types.

example:

```python
import voicemeeterlib
# Set event updates to occur every 50ms
# Listen for level updates only
with voicemeeterlib.api('banana', ratelimit=0.05, ldirty=True) as vm:
    ...
```

#### `vm.observer`

Use the Subject class to register an app as event observer.

The following methods are available:

-   `add`: registers an app as an event observer
-   `remove`: deregisters an app as an event observer

example:

```python
# register an app to receive updates
class App():
    def __init__(self, vm):
        vm.observer.add(self)
        ...
```

#### `vm.event`

Use the event class to toggle updates as necessary.

The following properties are available:

-   `pdirty`: boolean
-   `mdirty`: boolean
-   `midi`: boolean
-   `ldirty`: boolean

example:

```python
vm.event.ldirty = True

vm.event.pdirty = False
```

Or add, remove a list of events.

The following methods are available:

-   `add()`
-   `remove()`
-   `get()`

example:

```python
vm.event.remove(["pdirty", "mdirty", "midi"])

# get a list of currently subscribed
print(vm.event.get())
```

## Remote class

`voicemeeterlib.api(KIND_ID: str)`

You may pass the following optional keyword arguments:

-   `sync`: boolean=False, force the getters to wait for dirty parameters to clear. For most cases leave this as False.
-   `ratelimit`: float=0.033, how often to check for updates in ms.
-   `pdirty`: boolean=False, parameter updates
-   `mdirty`: boolean=False, macrobutton updates
-   `midi`: boolean=False, midi updates
-   `ldirty`: boolean=False, level updates

Access to lower level Getters and Setters are provided with these functions:

-   `vm.get(param, is_string=False)`: For getting the value of any parameter. Set string to True if getting a property value expected to return a string.
-   `vm.set(param, value)`: For setting the value of any parameter.

example:

```python
vm.get('Strip[2].Mute')
vm.set('Strip[4].Label', 'stripname')
vm.set('Strip[0].Gain', -3.6)
```

Access to lower level polling functions are provided with the following property objects:

##### `vm.pdirty`

True iff a parameter has been updated.

##### `vm.mdirty`

True iff a macrobutton has been updated.

##### `vm.ldirty`

True iff a level has been updated.


### Errors

-   `errors.VMError`: Exception raised when general errors occur.
-   `errors.InstallError`: Exception raised when installation errors occur.
-   `errors.CAPIError`: Exception raised when the C-API returns error values.
    -   Error codes are stored in {Exception Class}.code. For a full list of error codes [check the VoicemeeterRemote header file][Voicemeeter Remote Header].


### Logging

It's possible to see the messages sent by the interface's setters and getters, may be useful for debugging.

example:
```python
import voicemeeterlib

logging.basicConfig(level=logging.DEBUG)

with voicemeeterlib.api("banana") as vm:
        ...
```


### Run tests

To run all tests:

```
pytest -v
```

### Official Documentation

-   [Voicemeeter Remote C API](https://github.com/onyx-and-iris/Voicemeeter-SDK/blob/update-docs/VoicemeeterRemoteAPI.pdf)


[Voicemeeter Remote Header]: https://github.com/onyx-and-iris/Voicemeeter-SDK/blob/update-docs/VoicemeeterRemote.h