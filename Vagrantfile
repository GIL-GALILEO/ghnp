Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/trusty64"

  config.vm.network :forwarded_port, guest: 8000, host: 5000
  config.vm.network :forwarded_port, guest: 8080, host: 5080

  config.vm.network :private_network, ip: '192.168.50.50'

  config.vm.synced_folder '.', '/opt/chronam', nfs: true

  config.vm.provider :virtualbox do |v, override|
    v.memory = 2048
    v.gui = false
    # box customizations for speed
    v.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
    v.customize ['modifyvm', :id, '--audio', 'none']
    v.customize ['modifyvm', :id, '--clipboard', 'bidirectional']
    v.customize ['modifyvm', :id, '--usb', 'off']
    v.customize ['modifyvm', :id, '--ioapic', 'on']
  end

end
