#!/bin/sh

# A simple Bash shell script that installs packages depended on by AstroNinja
# Created by: Tom Mullins
# Created: 10/01/2018
# Modified: 05/10/2023


# Testing for addition of an option to install on Fedora

# Getting which distro the user is running
if [ -f /etc/os-release ]; then
    # freedesktop.org and systemd
    . /etc/os-release
    OS=$NAME

#echo $OS

# If the user is running Fedora
if [ "$OS" = "Fedora Linux" ] ; then
  # First, we need to install the proper python 3 Libraries
  sudo dnf install -y python3-pip python3-qt5 python3-dateutil  python3-qt5-webengine python3-setuptools

  # Next we install the libaries installed by pip
  python3 -m pip install matplotlib lxml scrapy

  # removes the folder, then copies the files to a . folder.
  rm -rf /home/$USER/.AstroNinja
  mkdir /home/$USER/.AstroNinja

  cp -r ./* /home/$USER/.AstroNinja

  # moving the desktop shortcut to the desktop
  mv /home/$USER/.AstroNinja/AstroNinja.desktop /home/$USER/Desktop/

  # Making both the desktop file and AstroNinjaMain.py executable
  chmod +x /home/$USER/Desktop/AstroNinja.desktop
  chmod +x /home/$USER/.AstroNinja/AstroNinjaMain.py

else
  # First, we need to install the proper python 3 Libraries
  sudo apt-get install -y python3-pip python3-pyqt5 python3-dateutil python3-pyqt5.qtwebengine python3-setuptools python3-matplotlib python3-lxml python3-scrapy

  # Next we install the libaries installed by pip
  # Commenting out because Ubuntu 23.04 changes the way python packages have to be installed.
  #python3 -m pip install matplotlib lxml scrapy

  # removes the folder, then copies the files to a . folder.
  rm -rf /home/$USER/.AstroNinja
  mkdir /home/$USER/.AstroNinja

  cp -r ./* /home/$USER/.AstroNinja

  # moving the desktop shortcut to the desktop
  mv /home/$USER/.AstroNinja/AstroNinja.desktop /home/$USER/Desktop/

  # Making both the desktop file and AstroNinjaMain.py executable
  chmod +x /home/$USER/Desktop/AstroNinja.desktop
  chmod +x /home/$USER/.AstroNinja/AstroNinjaMain.py

fi

  #echo $OS
  # If the user is running Linux Mint
  if [ "$OS" = "Linux Mint" ] ; then
      # Removing an uneeded package that causes formatting errors in Linux Mint
      sudo apt-get remove qt5ct ;
  fi





fi
