import os

class Config:
    SECRET_KEY = os.environ.get('SESSION_SECRET') or 'workersconnect-secret-key-2024'

    # Render persistent disk path
    DB_PATH = "/data/workersconnect.db"

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + DB_PATH
    SQLALCHEMY_TRACK_MODIFICATIONS = False