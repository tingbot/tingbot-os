# this file is run on the pi

set -x
set -o errexit
set -o pipefail

sudo apt-get -y update
sudo apt-get -y install python-pip python-dev 
sudo apt-get -y install avahi-daemon

sudo pip install pillow==2.9.0 requests==2.7.0

# install tbprocessd
(
  git clone https://github.com/tingbot/tbprocessd.git
  cd tbprocessd
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
  git clone https://github.com/tingbot/tide.git tide
  sudo cp -R tide/Tide/tingbot /usr/lib/python2.7/dist-packages
  rm -rf tide
)

# sudo REPO_URI=https://github.com/notro/rpi-firmware rpi-update 4815829b3f98e1b9c2648d9643dfe993054923ce
# This version of rpi-update gets the FBTFT kernel with SPI DMA
# See https://github.com/notro/fbtft/wiki#install
sudo REPO_URI=https://github.com/notro/rpi-firmware rpi-update
