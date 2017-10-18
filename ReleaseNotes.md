# v0.2 (10/20/2017)
# Release Notes

## Notable Changes
The Barcelona Release (v 0.2) of the Bluetooth micro service includes the following:
* Added configurable option to enable automatic upload of Device Profiles
* POM changes for appropriate repository information for distribution/repos management, checkstyle plugins, etc.
* Removed all references to unfinished DeviceManager work as part of Dell Fuse
* Added Dockerfile for creation of micro service targeted for ARM64
* Consolidated Docker properties files to common directory

## Bug Fixes
* Fixed Device equality logic
* Added check for service existence after initialization to Base Service

 - [#15](https://github.com/edgexfoundry/device-bluetooth/pull/15) - Remove staging plugin contributed by Jeremy Phelps ([JPWKU](https://github.com/JPWKU))
 - [#14](https://github.com/edgexfoundry/device-bluetooth/pull/14) - Dockerfile fixes contributed by Tyler Cox ([trcox](https://github.com/trcox))
 - [#13](https://github.com/edgexfoundry/device-bluetooth/pull/13) - Adds null check in BaseService contributed by Tyler Cox ([trcox](https://github.com/trcox))
 - [#12](https://github.com/edgexfoundry/device-bluetooth/pull/12) - Fixes Maven artifact dependency path contributed by Tyler Cox ([trcox](https://github.com/trcox))
 - [#11](https://github.com/edgexfoundry/device-bluetooth/pull/11) - added staging and snapshots repos to pom along with nexus staging mav… contributed by Jim White ([jpwhitemn](https://github.com/jpwhitemn))
 - [#10](https://github.com/edgexfoundry/device-bluetooth/pull/10) - Removed device manager url refs in properties files contributed by Jim White ([jpwhitemn](https://github.com/jpwhitemn))
 - [#9](https://github.com/edgexfoundry/device-bluetooth/pull/9) - Added support for aarch64 arch contributed by ([feclare](https://github.com/feclare))
 - [#8](https://github.com/edgexfoundry/device-bluetooth/pull/8) - Added support for aarch64 arch contributed by ([feclare](https://github.com/feclare))
 - [#7](https://github.com/edgexfoundry/device-bluetooth/pull/7) - Add option to auto-add default device profiles contributed by ([Smit-Sheth](https://github.com/Smit-Sheth))
 - [#6](https://github.com/edgexfoundry/device-bluetooth/pull/6) - Fixes device comparison logic contributed by Tyler Cox ([trcox](https://github.com/trcox))
 - [#5](https://github.com/edgexfoundry/device-bluetooth/pull/5) - Adds Docker build capability contributed by Tyler Cox ([trcox](https://github.com/trcox))
 - [#4](https://github.com/edgexfoundry/device-bluetooth/pull/4) - Add distributionManagement for artifact storage contributed by Tyler Cox ([trcox](https://github.com/trcox))
 - [#3](https://github.com/edgexfoundry/device-bluetooth/pull/3) - fix change of packaging for schedule clients contributed by Jim White ([jpwhitemn](https://github.com/jpwhitemn))
 - [#2](https://github.com/edgexfoundry/device-bluetooth/pull/2) - Fixes Service Name for Dev Env contributed by Tyler Cox ([trcox](https://github.com/trcox))
 - [#1](https://github.com/edgexfoundry/device-bluetooth/pull/1) - Contributed Project Fuse source code contributed by Tyler Cox ([trcox](https://github.com/trcox))
