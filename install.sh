#!/bin/bash

echo "Install Pip cho Python"
sudo apt -y install python3-pip
pip3 install --upgrade pip

echo "Install Pre-Opencv"
sudo apt -y update && sudo apt-get -y upgrade
sudo apt install -y build-essential cmake unzip pkg-config
sudo apt install -y libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt install -y libxvidcore-dev libx264-dev
sudo apt install -y libfontconfig1-dev libcairo2-dev
sudo apt install -y libgdk-pixbuf2.0-dev libpango1.0-dev
sudo apt install -y libgtk2.0-dev libgtk-3-dev
sudo apt install -y libatlas-base-dev gfortran
sudo apt install -y libhdf5-dev libhdf5-serial-dev libhdf5-103
sudo apt install -y libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
sudo apt install -y python3-dev
sudo apt install -y libjpeg-dev libpng-dev libtiff-dev
sudo apt install -y libgtk-3-dev
sudo apt install -y libcanberra-gtk*
pip3 install cython
pip3 install wheel

echo "=====================> Install Numpy"

#---------------------------------------------------------
echo "====================> Install Opencv"
pip3 install opencv-python

echo "Install Tkinter"
sudo apt install -y python3-tk

echo "====================> Install More"
pip3 install requests==2.18.4
pip3 install getmac==0.8.2
pip3 install scipy
pip3 install Pillow
pip3 install geocoder
pip3 install playsound

