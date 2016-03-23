import os


# default config
class BaseConfig(object):
    DEBUG = False
    # shortened for readability
    SECRET_KEY = 'xr\xb5\x96\xac\x02\xe8)W#\xea\xe6\xb5\xc2\xeb6\x8b\xe1\xa2L\x10{\x19\xf2'
    SQLALCHEMY_DATABASE_URI =os.environ['DATABASE_URL']
    #print SQLALCHEMY_DATABASE_URI


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False