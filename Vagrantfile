# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.network "public_network", ip: "192.168.1.10"
#  config.vm.network "private_network", ip: "192.168.10.10"
#  config.vm.name = "exercise"
  config.vm.provision "ansible" do |ansible|
    # Disable default limit to connect to all the nodes
    ansible.limit = "all"
    ansible.playbook = "playbook.yml"
    ansible.compatibility_mode = "2.0"
    ansible.become = true
#   ansible.galaxy_role_file = "requirements.yml"
  end
end
