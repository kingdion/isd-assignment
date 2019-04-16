# ISD Assignment #1 

* Dion Misic
* Xavier Carmo
* Amara Tut 
* Tyrone Huang 
* Nicholas Zay
* Chris Tran

---

# Installation 

## Python Requirements

You need to have a working version of python installed.
Our project is built to run on Python 3.7. Please follow the instructions [here](https://wiki.python.org/moin/BeginnersGuide/Download) to install python to your machine or find the downloads [here](https://www.python.org/downloads/).

It is recommended to install our dependencies in a container so it does not interfer
with other installations of python, or your system level dependencies. 
Our recommendation is virtualenv. 

Navigate to the root directory of the project through the command-line: 

1. Install virtualenv

    `$ pip install virtualenv`

2. From the root of the project directory, (to create a new env) run:

    `$ virtualenv isd`

3. Use the environment by running:

    `$ source /isd/bin/activate`

4. Now you can install our dependencies using:

    `$ pip install -r requirements.txt`

## Setup Database

Our project is built using *postgres*. You can find a download of the postgres binaries [here](https://www.postgresql.org/download/).
There are many ways to install postgres and it depends on your operating system. It is recommended you find an installation that will work for your system. However, if you are running MacOS, we suggest this [graphical application that does some heavy lifting](https://postgresapp.com/).

When postgres is installed on your machine, you will need to create a database called "isd" before running the project.
You can do this through most of the graphical postgres interfaces, or alternatively through the commandline.

In the command line, run the following commands:

1. `$ psql` (opens postgres interpreter)
2. `CREATE DATABASE isd;`

You can now exit the postgres interpreter using `\q`.


## Running the Project
Once the isd database is created and the requirements are installed - 
From the root directory of the project, run:

`$ python run.py runserver`

If all is done correctly, a local webserver should be available to the browser at 127.0.0.1
   
---


# Schema Upgrade (migrations)

When changes are made to the database models, run:

`$ python run.py db migrate` - Updates schema version, creates update file in migrations/versions with changes to db

`$ python run.py db upgrade` - Actually runs the upgrade on the database 



