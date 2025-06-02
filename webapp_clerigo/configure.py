from os import getenv
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = getenv('SECRET_KEY')
DB_HOST = getenv("DB_HOST")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_DATABASE = getenv("DB_DATABASE")
DB_PORT= getenv("DB_PORT")
CLOUD_NAME = getenv('CLOUD_NAME')
API_KEY = getenv('API_KEY')
API_SECRET = getenv('API_SECRET')