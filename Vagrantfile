# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  def configure(c, addr, hostname)
    c.vm.box = "bento/ubuntu-16.04"
    c.vm.network :private_network, ip: addr
    c.vm.hostname = hostname
    c.vm.box_check_update = false
    c.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      vb.memory = 1024
    end
  end

  config.vm.define "istio1" do |c|
    configure c, "192.168.50.21", "istio1"
  end
  config.vm.define "istio2" do |c|
    configure c, "192.168.50.22", "istio2"
  end
  config.vm.define "istio3" do |c|
    configure c, "192.168.50.23", "istio3"
  end
end
