# this file is run on the pi

set -x
set -o errexit
set -o pipefail

sudo apt-get -y update

# need to free some space
sudo apt-get -y remove wolfram-engine

sudo apt-get -y install python-pip python-dev
sudo apt-get -y install avahi-daemon evtest tslib libts-bin

sudo pip install pip==8.0.3
sudo pip install wheel==0.29.0 setuptools==20.2.2
sudo pip install pillow==2.9.0 requests==2.7.0 evdev==0.5.0

# install tbprocessd
(
  git clone https://github.com/tingbot/tbprocessd.git
  cd tbprocessd
  sudo pip install -r requirements.txt
  sudo make install
  cd ..
  sudo rm -rf tbprocessd
)

# install tingbot-wifi util
(
  sudo update-rc.d tbwifisetup defaults
  sudo update-rc.d tbwifisetup enable
)

# add screen config to /boot/config.txt
(
  sudo tee -a /boot/config.txt > /dev/null <<EOF
dtparam=spi=on
dtoverlay=tingbot:xohms=80
EOF
)

# install tingbot libraries
(
  sudo pip install git+https://github.com/tingbot/tingbot-python.git@33cf3a850a1be405f731bb395d83a8e9697fc4bc
)

# add fbcon=map:10 to kernel cmdline
sudo sed -i '1 s/$/ fbcon=map:10/' /boot/cmdline.txt

# sudo REPO_URI=https://github.com/notro/rpi-firmware rpi-update 4815829b3f98e1b9c2648d9643dfe993054923ce
# This version of rpi-update gets the FBTFT kernel with SPI DMA
# See https://github.com/notro/fbtft/wiki#install
sudo rpi-update 31615deb9406ffc3ab823e76d12dedf373c8e087
