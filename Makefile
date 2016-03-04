.PHONY: build

BASE_IMG_URL := http://downloads.raspberrypi.org/raspbian/images/raspbian-2016-02-29/2016-02-26-raspbian-jessie.zip
BASE_IMG_NAME := $(basename $(notdir $(BASE_IMG_URL))).img

build: dl/$(BASE_IMG_NAME)
	chmod 600 tingbot.key
	rm -rf build
	mkdir build
	cp dl/$(BASE_IMG_NAME) build/disk.img
	expect -f vm-setup.expect
	expect -f vm-build.expect
	expect -f vm-cleanup.expect
	ditto -ck build/disk.img build/disk.img.zip

dl/$(BASE_IMG_NAME):
	mkdir -p dl
	curl --location -o dl/$(BASE_IMG_NAME).zip $(BASE_IMG_URL)
	ditto -kx dl/$(BASE_IMG_NAME).zip dl/zipfile
	mv dl/zipfile/*.img dl/$(BASE_IMG_NAME)
