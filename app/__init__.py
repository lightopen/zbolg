from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.login import LoginManager
from config import config
from flask.ext.bootstrap import Bootstrap
import os

# instance Class
mail = Mail()
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = "basic"
login_manager.login_view = 'auth.signin'

# create app with instace init
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    mail.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    # register blueprint
    from .main import main
    app.register_blueprint(main)
    from .auth import auth
    app.register_blueprint(auth, url_prefix="/auth")
    from .admin import admin
    app.register_blueprint(admin, url_prefix="/admin")

    return app

