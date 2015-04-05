# -*- mode: python-*-

Vagrant.configure('2') do |config|
  config.vm.provider "virtualbox" do |v, override|
    override.vm.box = 'Ubuntu 14.10'
    override.vm.box_url = "https://github.com/jose-lpa/packer-ubuntu_14.04/releases/download/v2.0/ubuntu-14.04.box"

    v.memory = 1024
    v.cpus = 2
  end
end
