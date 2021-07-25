#!/bin/sh

# A simple Bash shell script that installs packages depended on by AstroNinja
# Created by: Tom Mullins
# Created: 09/24/2020
# Modified: 07/25/2021

# Getting which distro the user is running
if [ -f /etc/os-release ]; then
    # freedesktop.org and systemd
    . /etc/os-release
    OS=$NAME

echo $OS

# If the user is running Linux Mint
if [ "$OS" = "Fedora" ] ; then
  # First, we need to install the proper python 3 Libraries
  sudo dnf install -y python3-pip python3-qt5 python3-dateutil  python3-qt5-webengine python3-setuptools

  # Next we install the libaries installed by pip
  python3 -m pip install matplotlib lxml scrapy

  # removes the folder, then copies the files to a . folder.
  rm -rf /home/$USER/.AstroNinja
  mkdir /home/$USER/.AstroNinja

  cp -r /home/$USER/Downloads/AstroNinja-Stable/* /home/$USER/.AstroNinja

else
  # First, we need to install the proper python 3 Libraries
  sudo apt-get install -y python3-pip python3-pyqt5 python3-dateutil python3-tk python3-pyqt5.qtwebengine python3-setuptools

  # Next we install the libaries installed by pip
  python3 -m pip install matplotlib lxml scrapy

  # removes the folder, then copies the files to a . folder.
  rm -rf /home/$USER/.AstroNinja
  mkdir /home/$USER/.AstroNinja

  cp -r /home/$USER/Downloads/AstroNinja-Stable/* /home/$USER/.AstroNinja
  fi
fi
