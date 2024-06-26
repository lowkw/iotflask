import os
from flask import Flask
from flask_cors import CORS
from .models import db
from .oauth2 import config_oauth
from .routes import bp


def create_app(config=None):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    # load default configuration
    app.config.from_object('website.settings')

    # load environment configuration
    if 'WEBSITE_CONF' in os.environ:
        app.config.from_envvar('WEBSITE_CONF')

    # load app specified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)

    setup_app(app)
    return app


def setup_app(app):
    # Create tables if they do not exist already
    # @app.before_first_request
    # def create_tables():
    #    db.create_all()

    with app.app_context():
        db.init_app(app)
        db.create_all()
        config_oauth(app)
        app.register_blueprint(bp, url_prefix='')
