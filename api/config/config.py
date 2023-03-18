import os
from decouple import config
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

import re

uri = config("DATABASE_URL") # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgressql://", 1)
#rest of connection code using the connection string `uri`

 
class Config:
     SECRET_KEY = config('SECRET_KEY', 'secret')
     JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=40)
     JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=40)
     JWT_SECRET_KEY = config('JWT_SECRET_KEY')
     
class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(BASE_DIR, 'db.sqlite3')
    
    
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
   

class ProdConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = uri
    DEBUG=config('DEBUG', cast=bool)
 

config_dict = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig
}