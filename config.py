class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Brian8053@@127.0.0.1:5432/taskapi_class'
    SECRET_KEY = 'some-secret-string'
    JWT_SECRET_KEY = 'some_random_key'

class ProductionConfig(Config):
    DEBUG = False
    