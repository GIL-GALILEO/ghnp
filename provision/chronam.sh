#!/bin/bash

# setup python and chronam related stuff
echo "Setting up Virtualenv"
virtualenv -p /usr/bin/python2.7 ENV

echo "Activating Virtualenv"
source /opt/chronam/ENV/bin/activate

echo "Copying pth file"
cp /opt/chronam/conf/chronam.pth ENV/lib/python2.7/site-packages/chronam.pth

echo "Installing requirements with Pip"
pip install -r /opt/chronam/requirements.pip --ignore-installed

# run db migrations
python /opt/chronam/core/manage.py migrate

# load static assets
python /opt/chronam/core/manage.py collectstatic --noinput

# ubuntu user should own django tmp dir
sudo chown -R ubuntu:ubuntu /var/tmp/django-cache/
