# this file is run on the pi

set -x
set -o errexit
set -o pipefail

sudo apt-get -y update
sudo apt-get -y install python-pip
sudo apt-get -y install avahi-daemon

# install tbprocessd
(
  git clone https://github.com/tingbot/tbprocessd.git
  cd tbprocessd
  sudo make install
  cd ..
  sudo rm -rf tbprocessd
)

# install avahi-daemon config
(
  sudo tee /etc/avahi/services/tingbot.service > /dev/null <<EOF
<?xml version="1.0" standalone='no'?><!--*-nxml-*-->
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">
<service-group>
  <name replace-wildcards="yes">%h</name>
  <service>
    <type>_tingbot-ssh._tcp</type>
    <port>22</port>
  </service>
</service-group>
EOF
)


# add screen config to /etc/modules
(
  sudo tee -a /etc/modules > /dev/null <<EOF
fbtft_device name=sainsmart32_spi gpios=reset:22,dc:27 rotate=270 speed=56000000 fps=50 debug=1
EOF
)

sudo REPO_URI=https://github.com/notro/rpi-firmware rpi-update 4815829b3f98e1b9c2648d9643dfe993054923ce
