## Getting Started
If you're familiar with django projects and have your environments already setup, skip to [installation](#installation).
If not, getting started is quick, easy, and rewarding; read on!

#### Python
The first step is to install and make sure python is working locally on your computer.

Python can be installed from the official [python website](https://www.python.org/). Just download the appropriate installer and version of python.
The python version can be found at the top of this page (Python 3.6 at the time of writing).

For windows systems: We'll be using python from the command line, so [add it to your path](https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-so-it-finds-my-modules-packages), if needed.

#### PIP and Virtual Environments
PIP is python's package installer, we'll be using it extensively. Additionally, create a separate python virtual environment to use for this project.
Follow [this excellent guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) to get started with pip and virtual environments.

You should be able to use pip commands and a separate blank virtual environment running python before continuing to the next steps.

#### PostgreSQL
The last piece is setting up your database system. We are going to be using [PostgreSQL](https://www.postgresql.org/about/).

PostgreSQL can be downloaded from the [official website](https://www.postgresql.org/download/). Make sure you install the appropriate version of Postgres (V 9.6 at the time of writing).
Don't worry if you install the wrong versions, you can always have multiple versions installed.

It might also be helpful to install [pgAdmin](https://www.pgadmin.org/) to make managing easier.

When you can see your Postgres server on a local port, you're done with this step.

### Installation
Once you have all the prerequisites in place, follow these steps to get an instance of the website setup locally:

1. Create a repository to your machine.
2. Create a virtual environment for this project.
3. Install the libraries in requirements.txt
   ```
   pip install -r requirements.txt
   ```
4. Make sure you have psycopg2 installed. By default pip should install the psycopg2 library in requirements.txt. [If not see below](#troubleshooting-psycopg2).

5. Create the database. The database, name, password and other parameters can be found in Ayan_P/settings.py
   ```
   createdb -h <host name> -p <port nunber> -U <username> <database name>
   ```
6. Create tables:
   ```
   python manage.py migrate
   ```
7. Create a superuser (admin) on your local database using a command script:
   ```
   python manage.py createsuperuser
   ```
8. Runserver
   ```
   python manage.py runserver
   ```
9. Go to your local host - 127.0.0.1:8000. Congratulations! You now have a functioning installation.
