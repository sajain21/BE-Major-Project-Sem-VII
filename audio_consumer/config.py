from os import environ, path
from dotenv import load_dotenv


# Load variables from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


# Database config
DATABASE_HOST = environ.get('host')
# don't use "username" due to some reason it is fetching it from somewhere else
DATABASE_USERNAME = environ.get('dbusername')
DATABASE_PASSWORD = environ.get('password')
DATABASE_NAME = environ.get('database')
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = environ.get('AWS_REGION')