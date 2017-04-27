#!/bin/sh -e

# install java
echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections
echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections
apt-get -y -q install oracle-java8-installer
update-java-alternatives -s java-8-oracle

# install solr
wget http://archive.apache.org/dist/lucene/solr/6.4.1/solr-6.4.1.tgz
tar -xvf solr-6.4.1.tgz

# copy solr config
sudo mkdir solr-6.4.1/server/solr/configsets/ghnp
sudo mkdir solr-6.4.1/server/solr/configsets/ghnp/conf
sudo mkdir solr-6.4.1/server/solr/configsets/ghnp/conf/lang
sudo cp /opt/chronam/solr/schema.xml solr-6.4.1/server/solr/configsets/ghnp/conf/schema.xml
sudo cp /opt/chronam/solr/solrconfig.xml solr-6.4.1/server/solr/configsets/ghnp/conf/solrconfig.xml
sudo cp solr-6.4.1/server/solr/configsets/basic_configs/conf/lang/stopwords_en.txt solr-6.4.1/server/solr/configsets/ghnp/stopwords_en.txt

# TODO: create a solr user

# start solr, creating collection
sudo bash solr-6.4.1/bin/solr start -c -force
sudo bash solr-6.4.1/bin/solr create -c ghnp -d ghnp -force