from flask import Blueprint
from .v1.routes import register_routes


def init_api(app):
    api_blueprint = Blueprint('api', __name__)
    register_routes(api_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
