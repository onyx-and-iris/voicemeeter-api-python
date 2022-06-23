# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Before any patch/minor/major bump all unit tests will be run to verify they pass.

## [Unreleased]

-   [x]

## [0.1.9] - 2022-06-21

### Added

-   Added sendtext to base class
-   script decorator added to util module.
-   README initial commit

### Fixed

-   bug fixed in FactoryBuilder strip, bus iterations.

### Changed

-   minor macrobutton refactor

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
