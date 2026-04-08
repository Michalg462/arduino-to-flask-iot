import os

from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    from . import landing
    app.register_blueprint(landing.bp)
    app.add_url_rule('/', endpoint='index')

    return app