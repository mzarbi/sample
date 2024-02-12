from flasgger import Swagger
from flask import Flask
from flask_cors import CORS

from .api import init_api


def create_app(config_name='development'):
    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': '*'}})
    Swagger(app)
    # Configuration can be set here
    app.config.from_object(f'app.config.{config_name.capitalize()}Config')

    # Initialize Blueprints
    init_api(app)

    # Initialize Access Control
    init_access_control(app)

    return app


def init_access_control(app):
    @app.before_request
    def before_request():
        pass
