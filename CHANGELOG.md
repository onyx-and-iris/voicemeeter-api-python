# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Before any major/minor/patch bump all unit tests will be run to verify they pass.

## [Unreleased]

-   [x]

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
