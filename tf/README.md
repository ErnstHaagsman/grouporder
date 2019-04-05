Grouporder AWS Development Environment
======================================

This repository contains the AWS configuration to set up a 
remote development environment for 
[grouporder](https://github.com/ErnstHaagsman/grouporder).

Instructions
------------

0.  First get [Terraform](https://terraform.io), and install it on
    your computer (make sure it's on your PATH)

0.  Clone this repository 

0.  Make sure you have a public key configured in the **AWS region** 
    where you'd like to spin up a grouporder dev environment. 

0.  Load the private key that matches the uploaded key in your SSH
    agent. On Ubuntu, just run `ssh-add` to add your id_rsa.
    
0.  Make sure you have a [`~/.aws/credentials` file.](http://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html)
    
0.  On the terminal (whether PyCharm built-in or regular) navigate
    to the folder where you've cloned this repository
    
0.  Run `terraform init`

0.  (Optional) Create a `terraform.tfvars` file to specify both the
    AWS public key name, and the AWS region.
    
0.  Run `terraform apply`


After running `terraform apply`, you should have an `ssh_config.out`
file. Copy the contents of this file to `~/.ssh/config`:

    cat ssh_config.out >> ~/.ssh/config
    
At this point you should be able to connect to all three hosts by
running `ssh management`, `ssh web`, or `ssh database`.