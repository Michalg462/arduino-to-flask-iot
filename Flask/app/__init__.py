from flask import Flask

from app.data_storage import start_comm_thread

# creation of the main app instance
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    # starting a thread that reads the values from arduino
    start_comm_thread()

    # definition of the index page
    from . import landing
    app.register_blueprint(landing.bp)
    app.add_url_rule('/', endpoint='index')

    return app