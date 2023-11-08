#!/bin/sh

# A simple Bash shell script that installs packages depended on by AstroNinja
# Created by: Tom Mullins
# Created: 09/24/2020
# Modified: 11/07/2023

# Getting which distro the user is running
if [ -f /etc/os-release ]; then
    # freedesktop.org and systemd
    . /etc/os-release
    OS=$NAME

echo $OS

# If the user is running Fedora
if [ "$OS" = "Fedora" ] ; then
  # First, we need to install the proper python 3 Libraries
  sudo dnf install -y python3-pip python3-qt5 python3-dateutil  python3-qt5-webengine python3-setuptools

  # Next we install the libaries installed by pip
  python3 -m pip install matplotlib lxml scrapy youtube-search-python 

  # removes the folder, then copies the files to a . folder.
  rm -rf /home/$USER/.AstroNinja
  mkdir /home/$USER/.AstroNinja

  cp -r /home/$USER/Downloads/AstroNinja-Stable/* /home/$USER/.AstroNinja

else
  # First, we need to install the proper python 3 Libraries
  sudo apt-get install -y python3-pip python3-pyqt5 python3-dateutil python3-pyqt5.qtwebengine python3-setuptools python3-matplotlib python3-lxml python3-scrapy

  # Next we install the libaries installed by pip
  #python3 -m pip install matplotlib lxml scrapy

  #installing the new library that is used in the newly implimented launch video fix. 
  # We have to install it via pip because it's a bit old and not in the Ubuntu repos.
  # I aplogize for having to do it this way.
  pip3 install youtube-search-python --break-system-packages 

  # removes the folder, then copies the files to a . folder.
  rm -rf /home/$USER/.AstroNinja
  mkdir /home/$USER/.AstroNinja

  cp -r /home/$USER/Downloads/AstroNinja-Stable/* /home/$USER/.AstroNinja
  fi
fi
