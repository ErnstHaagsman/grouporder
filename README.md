Group Order
===========

A RESTful API to organize ordering food together with coworkers.

Prerequisites
-------------

For local development, I'm using a Vagrant box. To develop in Vagrant, you need
to have both it and Virtualbox (or another compatible VM tool) installed:

- Get Vagrant from https://vagrantup.com
- Get Virtualbox from https://www.virtualbox.org/wiki/Downloads

Get started
-----------

To run group order locally, check out this repo and then run `vagrant up`.
After the box has come up, first activate the virtualenv, and migrate the 
database to the latest version:

    source ~/venv/bin/activate
    cd /vagrant/migrations
    pgmigrate migrate -t latest --conn postgresql://user:pass@host/db
    
You can configure the database credentials in the `setup.yml` Ansible playbook.
Defaults:

|Host        | Localhost  |
|Database    | grouporder |
|Username    | grouporder |
|Password    | hunter2    |

This makes the migrate command:

    pgmigrate migrate -t latest --conn postgresql://grouporder:hunter2@localhost/grouporder
    
Afterwards you can run the Flask application. You need to specify the database
URI using an environment variable:

    cd /vagrant/grouporder
    DATABASE_URI=postgresql://grouporder:hunter2@localhost/grouporder python server.py
    

In PyCharm
----------

Make sure you've started (and provisioned) the Vagrant box before. From within
PyCharm (Professional Edition only) you can do this by choosing Tools | Vagrant |
Up. 

1. Configure the interpreter: go to File | Settings (PyCharm | Settings on 
   macOS), then choose Project: grouporder, and Project Interpreter. Use the
   gear icon next to the interpreter dropdown, and choose 'Add Remote'. Pick
   'Vagrant', and then use `/home/vagrant/venv/bin/python` as the Python 
   interpreter path.
2. Mark the 'grouporder' folder as sources. Right-click it in the project tool
   window, choose 'Mark Directory as', and 'Sources'
3. Create a run configuration: go to Run | Edit Configurations. Use the green 
   '+', and choose 'Python'. Navigate to grouporder/server.py for script. And 
   then add the 'DATABASE_URI' environment variable.
   
Now when clicking either run or debug, the server should come alive.

To configure the database tool, make sure the database tool window is open: 
View | Tool Windows | Database. Then use the green '+' to add a data source,
choose Postgres, and then enter the DB credentials (see above for the defaults).
After configuring the database, you should get code completion for SQL 
statements in Python code.
   