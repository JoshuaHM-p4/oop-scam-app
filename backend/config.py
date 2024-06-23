import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    JWT_SECRET_KEY = 'your_jwt_secret_key'
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False