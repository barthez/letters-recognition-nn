#!/bin/sh

apt-get update

apt-get install python-dev gfortran python-distutils-extra python-setuptools

apt-get install python-scipy
apt-get install python-matplotlib

easy_install -U ffnet
easy_install -U networkx
