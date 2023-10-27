# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Before any major/minor/patch bump all unit tests will be run to verify they pass.

## [Unreleased]

-   [x]

## [2.5.0]

### Fixed

-   {Remote}.login() now has a configuratble timeout. Use timeout kwarg to set it. Defaults to 2 seconds.
-   Remote class section in README updated to include timeout kwarg.

## [2.4.8] - 2023-08-13

### Added

-   Error tests added in tests/test_errors.py
-   fn_name and code set as class attributes for CAPIError
-   Errors section in README updated.

### Changed

-   InstallError and CAPIError classes now subclass VMError

## [2.3.7] - 2023-08-01

### Changed

-   If the configs loader is passed an invalid config TOML it will log an error but continue to load further configs into memory.

## [2.3.2] - 2023-07-12

### Added

-   vban.{instream,outstream} tuples now contain classes that represent MIDI and TEXT streams.

### Fixed

-   apply_config() now performs a deep merge when extending a config with another.

## [2.3.0] - 2023-07-11

### Added

-   user configs may now extend other user configs. check `config extends` section in README.

## [2.2.0] - 2023-07-10

### Added

-   CAPIError class now stores fn_name, error code and message as class attributes.

### Changed

-   macrobutton capi calls now use error code -9 on AttributeError (using an old version of the API).

### Fixed

-   call to `self.vm_get_midi_message` now wrapped by {CBindings}.call.

## [2.1.1] - 2023-07-01

### Added

-   RecorderMode added to Recorder class. See Recorder section in README for new properties and methods.
    -   recorder.loop is now a forwarder method for recorder.mode.loop for backwards compatibility

-   RecorderArmStrip, RecorderArmBus mixed into Recorder class.

### Removed

-   Recorder.loop removed from documentation

### Changed

-   When out of bounds values are passed, log warnings instead of raising Errors. See [Issue #6][Issue 6].

## [2.0.0] - 2023-06-25

Where possible I've attempted to make the changes backwards compatible. The breaking changes affect two higher classes, Strip and Bus, as well as the behaviour of events. All other changes are additive or QOL aimed at giving more options to the developer. For example, every low-level CAPI call is now logged and error raised on Exception, you can now register callback functions as well as observer classes, extra examples to demonstrate different use cases etc.

The breaking changes are as follows:

### Changed

-   `strip[i].comp` now references StripComp class
    -   To change the comp knob you should now use the property `strip[i].comp.knob`
-   `strip[i].gate` now references StripGate class

    -   To change the gate knob you should now use the property `strip[i].gate.knob`

-   `bus[i].eq` now references BusEQ class

    -   To set bus[i].{eq,eq_ab} as before you should now use bus[i].eq.on and bus[i].eq.ab

-   by default, <strong>NO</strong> events are checked for. This is reflected in factory.FactoryBase defaultkwargs.
    -   This is a fundamental behaviour change from version 1.0 of the wrapper. It means the following:
        -   Unless any events are explicitly requested with an event kwarg the event emitter thread will not run automatically.
        -   Whether using a context manager or not, you can still initiate the event thread manually and request events with the event object.<br>
            see `events` example.

There are other non-breaking changes:

### Added

-   `strip[i].eq` added to PhysicalStrip
-   `strip[i].denoiser` added to PhysicalStrip
-   `Strip.Comp`, `Strip.Gate`, `Strip.Denoiser` sections added to README.
-   `Events` section in readme updated to reflect changes to events kwargs.
-   new comp, gate, denoiser and eq tests added to higher tests.
-   `levels` example to demonstrate use of the interface without a context manager.
-   `events` example to demonstrate how to interact with event thread/event object.
-   `gui` example to demonstrate GUI controls.
-   `{Remote}.observer` can be used in place of `{Remote}.subject` although subject will still work. Check examples.
-   Subject class extended to allow registering/de-registering callback functions (as well as observer classes). See `events` example.

### Changed

-   `comp.knob`, `gate.knob`, `denoiser.knob`, `eq.on` added to phys_strip_params in config.TOMLStrBuilder

    -   The `example.toml` config files have been updated to demonstrate setting new comp, gate and eq settings.

-   event kwargs can now be set directly. no need for `subs`. example: `voicemeeterlib.api('banana', midi=True})`

-   factorybuilder steps now logged in DEBUG mode.

-   now using a producer thread to send events to the updater thread.

-   module level loggers implemented (with class loggers as child loggers)

-   config.loader now checks `Path.home() / ".config" / "voicemeeter" / kind.name` for configs.
    -   note. `Path(__file__).parent / "configs" / kind.name,` was removed as a path to check.

### Fixed

-   All low level CAPI calls are now wrapped by CBindings.call() which logs any errors raised.
-   Dynamic binding of Macrobutton functions from the CAPI.
    Should add backwards compatibility with very old versions of the api. See [Issue #4][issue 4].
-   factory.request_remote_obj now raises a `VMError` if passed an incorrect kind.

## [1.0.0] - 2023-06-19

No changes to the codebase but it has been stable for several months and should already have been bumped to major version 1.0

I will move this commit to a separate branch in preparation for version 2.0.

## [0.9.0] - 2022-10-11

### Added

-   StripDevice and BusDevice mixins.
-   README updated to reflect changes.
-   Minor version bump

### Removed

-   device, sr properties for physical strip, bus moved into mixin classes

### Changed

-   Event class property setters added.
-   Event add/remove methods now accept multiple events.
-   bus levels now printed in observer example.

### Fixed

-   initialize channel comps in updater thread. Fixes bug when switching to a kind before any level updates have occurred.

## [0.8.0] - 2022-09-29

### Added

-   Logging level INFO set on all examples.
-   Minor version bump
-   vm.subject subsection added to README

### Changed

-   Logging module used in place of print statements across the interface.
-   time.time() now used to steady rate of updates in updater thread.

### Fixed

-   call to cache bug in updater thread

## [0.7.0] - 2022-09-03

### Added

-   tomli/tomllib compatibility layer to support python 3.10

### Removed

-   3.10 branch

## [0.6.0] - 2022-08-02

### Added

-   Keyword argument subs for voicemeeterlib.api. Initialize which events to sub to.
-   Event class added to misc. Toggle events, get list of currently subscribed.
-   voicemeeterlib.api section added to README in Base Module section.
-   observer example updated to reflect changes.

### Changed

-   By default no longer listen for level updates (high volume). Should be enabled explicitly.

## [0.5.0] - 2022-07-24

### Added

-   Midi class added to misc.
-   Midi added to observer notifications
-   Midi example added.
-   Midi section added to readme.
-   Minor version bump.

## [0.4.0] - 2022-07-21

### Added

-   asio, insert added to kind maps (maps patching parameters)
-   Patch added to misc
-   Option added to misc
-   Patch, option sections added to readme.
-   Patch, option unit tests added
-   alias property isdirty for is_updated in strip/bus levels

### Changed

-   make_strip_level_map, make_bus_level_map added.
-   observer example using isdirty

### Fixed

-   error message for vban.sr setter

## [0.3.0] - 2022-07-16

### Added

-   get() added to bus mode mixin. returns the current bus mode.
-   support for all strip level modes in observable thread
-   effects parameters mixed into physicalstrip, physicalbus, virtualbus classes
-   fx class to potato remote kind (for toggling reverb, delay)
-   test_configs to unit tests
-   test_factory to unit tests
-   fx, xy tests added to higher tests.

### Changed

-   observer example switched from strip to bus. easier to test a single input for several buses.

### Fixed

-   is_updated in strip/bus levels now returns a bool, is level dirty or not?
-   for basic kind only, virtual bus now subclasses physical bus, since it is the only version you may
    attach a physical device to a virtual out.

### Removed

-   type checks

## [0.2.3] - 2022-07-09

### Changed

-   only compute strip_comp, bus_comp if ldirty.
-   switch from strip to bus in obs example.

### Fixed

-   bug in strip fadeto/fadeby
-   comp added to util.
-   range expressions in vban.

## [0.2.0] - 2022-07-02

### Added

-   obs added to examples
-   Readme updated to reflect changes.
-   device, gainlayers, levels, bus mode sections added.
-   minor version bump (probably should have been major since changes to ldirty effect client code)

### Changed

-   No longer passing data in ldirty notification.
-   rw changed to rew in recorder class to match capi

## [0.1.10] - 2022-06-28

### Added

-   pre-commit.ps1 added for use with git hook

### Fixed

-   mdirty added to observer updates
-   Error in cbindings

## [0.1.9] - 2022-06-21

### Added

-   Added sendtext to base class
-   script decorator added to util module.
-   README initial commit

### Changed

-   minor macrobutton refactor

### Fixed

-   bug fixed in FactoryBuilder strip, bus iterations.

## [0.1.8] - 2022-06-20

### Added

-   notify pdirty, ldirty now implemented.

### Changed

-   imports now isorted.
-   ratelimit now set at default 33ms.
-   ldirty modified, no longer sends comp, levels data

## [0.1.7] - 2022-06-18

### Added

-   added observable thread. (init_thread, end_thread methods added to base class)
-   added ldirty parameter
-   phys_in, virt_in, phys_out, virt_out properties added to KindMapClass
-   ratelimit default kwarg added
-   pre-commit.ps1 added for use with git hook
-   simple DSL example added

### Changed

-   str magic methods overriden in higher classes

### Fixed

-   bug in cbindings vm_set_parameter_multi argtypes

## [0.1.6] - 2022-06-17

### Added

-   Higher class device implemented.
-   BusLevel, StripLevel classes added to bus, strip modules respectively.
-   float_prop, bus_mode_prop meta functions added to util module.
-   bus mode mixin added to bus factory method
-   type, version implemented into base class.

### Fixed

-   Bug in factory builder

## [0.1.5] - 2022-06-14

### Added

-   docstrings added

### Changed

-   Gainlayer mixed in only if potato kind in Strip factory method.

## [0.1.4] - 2022-06-12

### Added

-   TOMLStrBuilder class added to config module. Builds a default config as a string for toml parser.
-   dataextraction_factory, TOMLDataExtractor added to config module. This allows option for other parser in future.

## [0.1.3] - 2022-06-09

### Added

-   Added type hints to base module
-   Higher classes Bus, PhysicalBus, VirtualBus implemented
-   bus module entry point defined.
-   Higher class Command implemented
-   Config module added. Loader class implemented for tracking configs in memory.
-   config entry point defined
-   Higher classes Strip, PhysicalStrip, VirtualStrip implemented
-   strip module entry point defined
-   Higher classes Vban, VbanInstream, VbanOutstream implemented
-   A common interface (IRemote) defined. Bridges base to higher classes.

## [0.1.2] - 2022-06-07

### Added

-   Implement creation class steps as command pattern

### Changed

-   Added progress report to FactoryBuilder

## [0.1.1] - 2022-06-06

### Added

-   move class creation into FactoryBuilder
-   creation classes now direct builder class
-   added KindId enum
-   added Subject module, but not yet implemented

### Changed

-   num_strip, num_bus properties added to KindMapClass

## [0.1.0] - 2022-06-05

### Added

-   cbindings defined
-   factory classes added, one for each kind.
-   inst module implemented (fetch vm path from registry)
-   kind maps implemented as dataclasses
-   project packaged with poetry and added to pypi.

[issue 4]: https://github.com/onyx-and-iris/voicemeeter-api-python/issues/4
[Issue 6]: https://github.com/onyx-and-iris/voicemeeter-api-python/issues/6
