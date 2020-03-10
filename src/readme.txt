# IN THE POSTGRES CONSOLE DO THE FOLLOWING

CREATE DATABASE aws;
\c aws;
CREATE USER root WITH PASSWORD 'root';

ALTER ROLE root SET client_encoding TO 'utf8';
ALTER ROLE root SET default_transaction_isolation TO 'read committed';
ALTER ROLE root SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE aws TO root;


# REQUIRED PACKAGES PIP
Django==3.0.4
psycopg2==2.8.4

# IF ERRORS IN INSTALLING PSYCOPG2 
sudo apt-get install libpq-dev

# TO RUN DO THE FOLLOWING COMMANDS
python manage.py makemigrations # This command converts the Object Oriented DDL code to SQL
python manage.py migrate # This command would execute the SQL queries and create the database
python manage.py runserver # This will start the python server

# TO ACCESS THE DJANGO ADMIN AT localhost:8000/admin, make sure you have a superuser
python manage.py createsuperuser
