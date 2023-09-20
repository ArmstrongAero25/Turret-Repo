# Turret Repo

This repo is for a small project I am working on:

The aim is to build and program a fully operational sentry turret/gun (It's a NERF gun!!!)

This is a colossal WIP but there will be many improvements to come.


# RASPBERRY PI TERMINAL COMMANDS TO OPERATE CAMERA:

sudo modprobe bcm2835-v4l2

pip uninstall opencv-python

This needs to be done as I need to install: opencv-contrib-python through pip install opencv-contrib-python

The Above doesn't work


#This Might Work

git clone --recursive https://github.com/opencv/opencv-python.git

cd opencv-python

export ENABLE_CONTRIB=1

pip wheel . --verbose
