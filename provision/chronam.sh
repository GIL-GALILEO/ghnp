#!/bin/bash

# setup python and chronam related stuff
echo "Setting up Virtualenv"
virtualenv -p /usr/bin/python2.7 ENV

echo "Activating Virtualenv"
source /var/www/ghnp/code/ENV/bin/activate

echo "Copying pth file"
cp /opt/chronam/conf/chronam.pth ENV/lib/python2.7/site-packages/chronam.pth

echo "Installing requirements with Pip"
pip install -r requirements.pip
