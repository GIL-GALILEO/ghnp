#!/bin/bash

# setup python and chronam related stuff
echo "Setting up Virtualenv"
virtualenv -p /usr/bin/python2.7 /opt/chronam/ENV

echo "Activating Virtualenv"
source /opt/chronam/ENV/bin/activate

echo "Creating pth file"
echo '/opt' > /opt/chronam/ENV/lib/python2.7/site-packages/chronam.pth

echo "Installing requirements with Pip"
python -m pip install -r /opt/chronam/requirements.pip --ignore-installed

# run db migrations
python /opt/chronam/core/manage.py migrate

# load static assets
python /opt/chronam/core/manage.py collectstatic --noinput

# load ChronAm database data
python /opt/chronam/core/manage.py chronam_sync --skip-essays

# load DLG specific data
python /opt/chronam/core/manage.py loaddata regions
python /opt/chronam/core/manage.py loaddata newspaper_types
python /opt/chronam/core/manage.py loaddata awardee
python /opt/chronam/core/manage.py loaddata funding_sources

# refine data
python /opt/chronam/core/manage.py refine_places

# create and own django tmp dir
# mkdir /var/tmp/django_cache/
# chown -R vagrant:vagrant /var/tmp/

