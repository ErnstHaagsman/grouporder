#!/usr/bin/env bash

cd ~

sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:ansible/ansible
sudo apt update
sudo apt install -y ansible git

git clone https://github.com/ErnstHaagsman/grouporder

cp deploy.yml grouporder/deploy.yml

cd grouporder

ansible-playbook -i ~/inventory deploy.yml
