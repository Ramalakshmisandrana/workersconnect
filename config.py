import os

class Config:
    SECRET_KEY = os.environ.get('SESSION_SECRET') or 'workersconnect-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///workersconnect.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
