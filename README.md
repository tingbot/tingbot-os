Tingbot SD card build system
============================

This system builds an SD card image ready to flash. The base is the Raspbian distribution, on which Tingbot-specific stuff is added. The image is booted inside an ARM emulator, using the vm-setup, vm-build, and vm-cleanup scripts.

The build.sh script is where the 'real' setup goes.

Requirements
------------

- qemu

  `brew install qemu`
  
Usage
-----

Just run `make`. The first run might take a while, as the raspbian image must be downloaded. Subsequent runs will be faster.
