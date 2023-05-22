# config.py

import os

class Config:
    SECRET_KEY = 'your-secret-key'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///your-database-file.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
