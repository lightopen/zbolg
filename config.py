import os

basedir = os.path.abspath(os.path.dirname(__file__))

# parent class
class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASK_MAIL_SUBJECT_PREFIX = "[System]"
    FLASK_MAIL_SENDER = os.environ.get("FLASK_MAIL_SENDER")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASK_ADMIN = os.environ.get("FLASK_ADMIN")
    @staticmethod
    def init_app(app):
        pass

# design model
class DesignConfig(Config):
    DEBUG = True
    MAIL_SERVER = "smtp.126.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USE_SSL= True
    MAIL_USERNAME = os.environ.get("FLASK_ADMIN")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir, 'zbolg.sqlite')

config = {'default': DesignConfig}
