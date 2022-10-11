# -*- encoding: utf-8 -*-
import os
from decouple import config
from dotenv import load_dotenv




class Config(object):
    DEBUG = False
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')
    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600
 
    # Mysql  database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config('DB_ENGINE', default='sqlite'),
        config('MYSQL_USER', default=str(os.getenv('MYSQL_USER'))),
        config('MYSQL_PASSWORD', default=str(os.getenv('MYSQL_PASSWORD'))),
        config('MYSQL_URL', default=str(os.getenv('MYSQL_URL'))),
        config('MYSQL_PORT', default=str(os.getenv('MYSQL_PORT'))),
        config('MYSQL_DB', default=str(os.getenv('MYSQL_DB')))
    )


class ProductionConfig(Config):
    load_dotenv() 
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600 
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Mysql  database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config('DB_ENGINE', default='sqlite'),
        config('MYSQL_USER', default=str(os.getenv('MYSQL_USER'))),
        config('MYSQL_PASSWORD', default=str(os.getenv('MYSQL_PASSWORD'))),
        config('MYSQL_URL', default=str(os.getenv('MYSQL_URL'))),
        config('MYSQL_PORT', default=str(os.getenv('MYSQL_PORT'))),
        config('MYSQL_DB', default=str(os.getenv('MYSQL_DB')))
    )

class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
