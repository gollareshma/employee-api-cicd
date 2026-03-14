import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    MYSQL_HOST = os.getenv("DB_HOST", "localhost")
    MYSQL_USER = os.getenv("DB_USER", "admin")
    MYSQL_PASSWORD = os.getenv("DB_PASSWORD", "password")
    MYSQL_DB = os.getenv("DB_NAME", "employeedb")

    JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key-123456789012345")

    TESTING = os.getenv("FLASK_ENV") == "testing"