.PHONY: build

BASE_IMG_URL := http://downloads.raspberrypi.org/raspbian/images/raspbian-2015-05-07/2015-05-05-raspbian-wheezy.zip

build: dl/base.img
	chmod 600 tingbot.key
	rm -rf build
	mkdir build
	cp dl/base.img build/disk.img
	expect -f vm-setup.expect
	expect -f vm-build.expect
	expect -f vm-cleanup.expect

dl/base.img:
	mkdir -p dl
	curl --location -o dl/base.zip $(BASE_IMG_URL)
	ditto -kx dl/base.zip dl/zipfile
	mv dl/zipfile/*.img dl/base.img
