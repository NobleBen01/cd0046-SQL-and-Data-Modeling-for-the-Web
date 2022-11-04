import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
connection_string="postgresgl:///"+os.path.join(basedir,'fyyur.db')


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:09030993500@localhost:5432/fyyur'
SQLALCHEMY_TRACK_MODIFICATIONS = False
