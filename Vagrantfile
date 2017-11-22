Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-16.04"

  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.network "forwarded_port", guest: 5432, host: 5678

  config.vm.provision "ansible_local" do |a|
    a.playbook = "setup.yml"
  end
end
