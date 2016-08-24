DEV SETUP

vagrant up
export DJANGO_SETTINGS_MODULE=chronam.settings
sudo service jetty start
django-admin runserver 0.0.0.0:8000

CHRONAM ENV SETUP

ubuntu/trusty64 vagrant box

vagrant up
vagrant ssh

give vagrant box at least 1024 MB memory

sudo apt-get install python-dev python-virtualenv mysql-server libmysqlclient-dev apache2 libapache2-mod-wsgi libxml2-dev libxslt-dev libjpeg-dev git-core graphicsmagick build-essential

sudo mkdir /opt/chronam
sudo chown $USER:users /opt/chronam
git clone https://github.com/LibraryOfCongress/chronam.git /opt/chronam

change shared dir to /opt/chronam in vagrantfile and reload

wget http://archive.apache.org/dist/lucene/solr/4.10.4/solr-4.10.4.tgz

tar zxvf solr-4.10.4.tgz
sudo mv solr-4.10.4/example/ /opt/solr

sudo useradd -d /opt/solr -s /bin/bash solr
sudo chown solr:solr -R /opt/solr

sudo cp /opt/chronam/conf/jetty7.sh /etc/init.d/jetty
sudo chmod +x /etc/init.d/jetty

sudo cp /opt/chronam/conf/schema.xml /opt/solr/solr/collection1/conf/schema.xml
sudo cp /opt/chronam/conf/solrconfig.xml /opt/solr/solr/collection1/conf/solrconfig.xml

sudo cp /opt/chronam/conf/jetty-ubuntu /etc/default/jetty
sudo service jetty start

[dont install/config apache]

then continue: https://github.com/LibraryOfCongress/chronam/blob/master/README.md#install

fix settings.py to refer to solr on port 8080
