# this file is run on the pi

set -x
set -o errexit
set -o pipefail

sudo apt-get -y update

# need to free some space
sudo apt-get -y remove wolfram-engine

# sudo apt-get -y install python-pip python-dev
# sudo apt-get -y install avahi-daemon evtest tslib libts-bin

# sudo pip install pip==8.0.3
# sudo pip install wheel==0.29.0 setuptools==20.2.2
# sudo pip install pillow==2.9.0 requests==2.7.0 evdev==0.5.0

# install tbprocessd
(
  # sudo pip install git+https://github.com/tingbot/tbprocessd.git@37441396607103ece37f19ddf2595e9f55cad353
)

# install tingbot-wifi util
(
  # sudo update-rc.d tbwifisetup defaults
  # sudo update-rc.d tbwifisetup enable
)

# add screen config to /boot/config.txt
(
#   sudo tee -a /boot/config.txt > /dev/null <<EOF
# dtparam=spi=on
# dtoverlay=tingbot:xohms=80
# EOF
)

# install tingbot libraries
(
  # sudo pip install git+https://github.com/tingbot/tingbot-python.git@41c560637c9243f452dda199c733afbc92f657fc
)

# add fbcon=map:10 to kernel cmdline
# sudo sed -i '1 s/$/ fbcon=map:10/' /boot/cmdline.txt
