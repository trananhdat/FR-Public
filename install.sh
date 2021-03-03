#!/bin/bash

echo "Install Pip cho Python"
sudo apt-get -y install python3-pip

echo "Install Pre-Opencv"
sudo apt-get -y update && sudo apt-get -y upgrade
sudo apt-get install -y build-essential cmake unzip pkg-config
sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install -y libxvidcore-dev libx264-dev
sudo apt-get install -y libfontconfig1-dev libcairo2-dev
sudo apt-get install -y libgdk-pixbuf2.0-dev libpango1.0-dev
sudo apt-get install -y libgtk2.0-dev libgtk-3-dev
sudo apt-get install -y libatlas-base-dev gfortran
sudo apt-get install -y libhdf5-dev libhdf5-serial-dev libhdf5-103
sudo apt-get install -y libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
sudo apt-get install -y python3-dev
sudo apt-get install -y libjpeg-dev libpng-dev libtiff-dev
sudo apt-get install -y libgtk-3-dev
sudo apt-get install -y libcanberra-gtk*

echo "=====================> Install Numpy"
pip3 install numpy==1.19.5
#---------------------------------------------------------
echo "====================> Install Opencv"
sudo apt-get install -y python3-opencv

echo "Install Tkinter"
sudo apt-get install -y python3-tk

echo "====================> Install More"
pip3 install requests==2.18.4
pip3 install getmac==0.8.2
pip3 install scipy==1.5.4
pip3 install Pillow==8.1.0
pip3 install geocoder
pip3 install playsound

