# this file is run on the pi

set -x
set -o errexit
set -o pipefail

sudo apt-get -y update
sudo apt-get -y install python-pip python-dev
sudo apt-get -y install avahi-daemon evtest tslib libts-bin

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
  git clone https://github.com/tingbot/tingbot-python.git tingbot-python
  sudo cp -R tingbot-python/tingbot /usr/lib/python2.7/dist-packages
  rm -rf tingbot-python
)

# add fbcon=map:10 to kernel cmdline
sudo sed -i '1 s/$/ fbcon=map:10/' /boot/cmdline.txt

# sudo REPO_URI=https://github.com/notro/rpi-firmware rpi-update 4815829b3f98e1b9c2648d9643dfe993054923ce
# This version of rpi-update gets the FBTFT kernel with SPI DMA
# See https://github.com/notro/fbtft/wiki#install
sudo REPO_URI=https://github.com/notro/rpi-firmware rpi-update
