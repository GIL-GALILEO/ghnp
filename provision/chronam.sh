#!/bin/bash

# setup python and chronam related stuff
echo "Setting up Virtualenv"
virtualenv -p /usr/bin/python2.7 /var/www/ghnp/code/ENV
echo "Activating Virtualenv"
source /var/www/ghnp/code/ENV/bin/activate
echo "Copying pth file"
cp /var/www/ghnp/code/conf/chronam.pth /var/www/ghnp/code/ENV/lib/python2.7/site-packages/chronam.pth
echo "Installing requirements with Pip"
/var/www/ghnp/code/ENV/bin/pip install -r /var/www/ghnp/code/requirements.pip

# echo "Making directories"
# mkdir /var/www/ghnp/code/data/batches
# mkdir /var/www/ghnp/code/data/cache
# mkdir /var/www/ghnp/code/data/bib

# echo "Copying settings from template"
# cp '/var/www/ghnp/code/settings_template.py' '/var/www/ghnp/code/settings.py'

# echo "Running GHNP migrations and data loads"
# export DJANGO_SETTINGS_MODULE=dlg.settings.settings

# python /var/www/ghnp/code/core/manage.py migrate
# python /var/www/ghnp/code/core/manage.py loaddata initial_data
# python /var/www/ghnp/code/core/manage.py chronam_sync --skip-essays
# python /var/www/ghnp/code/core/manage.py collectstatic --noinput