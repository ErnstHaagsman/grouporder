Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-16.04"

  config.vm.provision "ansible_local" do |a|
    a.playbook = "setup.yml"
  end
end
