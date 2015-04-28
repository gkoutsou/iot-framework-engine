#!/bin/bash
### Author : Tommy Mattsson
### Purpose: Easy installation of needed software for our project that is part of the linux system rather than our own project

#Break on error
set -e


install_boot_script() {  # $1 is the script
   sudo cp $PWD/scripts/boot/$1 /etc/init.d
   if [ $? -ne 0 ]; then
      echo "Call the script from the project folder"
   else
      echo "iotf-rmq... Success!"
      sudo chmod +x /etc/init.d/$1
      sudo update-rc.d $1 defaults
   fi
}

echo "#################################################################"
echo "Installing misc dependencies"
echo "#################################################################"
#sudo apt-get install -yq xsltproc software-properties-commom python-pip libpython-dev
sudo apt-get install -yq xsltproc python-pip libpython-dev

echo "#################################################################"
echo "Installing openjdk-7"
echo "#################################################################"
sudo apt-get install -yq openjdk-7-jre-headless libwxgtk2.8-0

echo "#################################################################"
echo "Installing Erlang 16B1"
echo "#################################################################"
apt-get install -yq erlang

echo "#################################################################"
echo "Installing Nodejs together with npm"
echo "#################################################################"
sudo apt-get install python-software-properties python g++ make
sudo add-apt-repository ppa:chris-lea/node.js
sudo apt-get update -q
sudo apt-get install -yq nodejs

echo "#################################################################"
echo "Installing R"
echo "#################################################################"
sudo add-apt-repository "deb http://ftp.sunet.se/pub/lang/CRAN/bin/linux/ubuntu trusty/"
sudo apt-get update -q
sudo apt-get install \r-base

echo "#################################################################"
echo "Installing pip"
echo "#################################################################"
sudo pip install -r semantic-adapter/pip-freeze.txt

echo "#################################################################"
echo "Installing boot scripts"
echo "#################################################################"
install_boot_script "iotf-backend"
install_boot_script "iotf-es"
install_boot_script "iotf-rmq"

