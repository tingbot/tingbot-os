.PHONY: build

BASE_IMG_URL := http://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2016-03-18/2016-03-18-raspbian-jessie-lite.zip
BASE_IMG_NAME := $(basename $(notdir $(BASE_IMG_URL))).img

build: dl/$(BASE_IMG_NAME)
	chmod 600 tingbot.key
	rm -rf build
	mkdir build
	# clean up .DS_Store files
	find root -name ".DS_Store" -delete
	dpkg -b root/ build/tingbot-os.deb
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
