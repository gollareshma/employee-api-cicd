import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Config:
    # MySQL Database configuration
    MYSQL_HOST = os.getenv("DB_HOST")
    MYSQL_USER = os.getenv("DB_USER")
    MYSQL_PASSWORD = os.getenv("DB_PASSWORD")
    MYSQL_DB = os.getenv("DB_NAME")
    MYSQL_CURSORCLASS = "DictCursor"

    # JWT configuration
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_EXPIRY_HOURS = 24

    # Flask settings
    DEBUG = os.getenv("FLASK_ENV") == "development"