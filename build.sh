# this file is run on the pi

set -x
set -o errexit

sudo apt-get -y update
sudo apt-get -y install python-pip
