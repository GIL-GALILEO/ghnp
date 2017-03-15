Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/xenial64"

  config.vm.network :forwarded_port, guest: 8000, host: 5000
  # config.vm.network :forwarded_port, guest: 5432, host: 5532
  config.vm.network :forwarded_port, guest: 8983, host: 5983

  config.vm.synced_folder '.', '/var/www/ghnp'

  config.vm.provision "shell", inline: <<-SHELL

    sudo date > /etc/vagrant_provisioned_at

    # basic
    apt-get update
    apt-get upgrade
    apt-get -y -q install python-software-properties software-properties-common gcc htop git python-dev python-virtualenv libxml2-dev libxslt-dev libjpeg-dev git-core graphicsmagick python-lxml zlib1g-dev
    add-apt-repository ppa:webupd8team/java
    apt-get update

    # download current app code
    git clone https://github.com/mksndz/dlg-chronam.git /var/www/ghnp/code

  SHELL

  config.vm.provision :shell, path: 'provision/solr.sh'
  config.vm.provision :shell, path: 'provision/postgres.sh'
  config.vm.provision :shell, path: 'provision/chronam.sh'

end