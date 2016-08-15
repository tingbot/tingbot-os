Tingbot SD card build system
============================

[![Build Status](https://travis-ci.org/tingbot/tingbot-os.svg?branch=master)](https://travis-ci.org/tingbot/tingbot-os)

This repo builds two products:

- `tingbot-os.deb`: a deb package that can be installed onto Raspbian Jessie to create the 'Tingbot OS'.
- `disk.img`: an SD card image with tingbot-os.deb preinstalled, ready for flashing to an SD card. This image also includes some extra stuff specific to an initial install - a specific build of SDL, and a program for expanding the SD card partition on first boot. See [build.sh](build.sh).

### `tingbot-os.deb`

This file is used to upgrade an existing Tingbot. It's downloaded by [tbupgrade](root/usr/bin/tbupgrade).

### `disk.img`

The base is the Raspbian distribution, on which Tingbot-specific stuff is added. The image is booted inside an ARM emulator, using the vm-setup, vm-build, and vm-cleanup scripts. The build.sh script runs on the Pi, which is where `tingbot-os.deb` installed.

Requirements
------------

- qemu (and expect on linux)

  `brew install qemu` (MacOSX)  
  `sudo apt-get install qemu expect` (Debian/Ubuntu)

Usage
-----

Just run `make build`. The first run might take a while, as the raspbian image must be downloaded. Subsequent runs will be faster.
