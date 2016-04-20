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
  git reset --hard a18b0ed68236330119e28d86dcc836f96e0ddda9
  sudo make install
  cd ..
  sudo rm -rf tbprocessd
)

# install tingbot-wifi util
(
  sudo update-rc.d tbwifisetup defaults
  sudo update-rc.d tbwifisetup enable
)

# add screen config to /etc/modules
(
  sudo tee -a /etc/modules > /dev/null <<EOF
fbtft_device name=sainsmart32_spi gpios=reset:22,dc:27 rotate=270 speed=56000000 fps=50 debug=1
EOF
)

# install tingbot libraries
(
  git clone https://github.com/tingbot/tide.git tide
  cd tide
  git reset --hard f7691a7bf2b87e553cd06e33d9c8a8ede54b7972
  cd ..
  sudo cp -R tide/Tide/tingbot /usr/lib/python2.7/dist-packages
  rm -rf tide
)

sudo REPO_URI=https://github.com/notro/rpi-firmware rpi-update 4815829b3f98e1b9c2648d9643dfe993054923ce
