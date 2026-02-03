import os

class Config:
    SECRET_KEY = os.environ.get('SESSION_SECRET') or 'workersconnect-secret-key-2024'

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
