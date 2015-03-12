# -*- mode: python-*-

Vagrant.configure('2') do |config|
  config.vm.provider "virtualbox" do |v, override|
    override.vm.box = 'Ubuntu 14.10'
    override.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/utopic/current/utopic-server-cloudimg-i386-vagrant-disk1.box"

    v.memory = 1024
    v.cpus = 2
  end
end
