import os
from dotenv import load_dotenv

# Load variables from .env if present
load_dotenv()

class Config:

    # Database configuration
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "employeedb")

    # JWT Secret
    JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-key-1234567890123456")

    # Flask settings
    FLASK_ENV = os.getenv("FLASK_ENV", "development")