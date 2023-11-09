import os, sys

def set_cwd():
    cwd = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cwd)

from flask import Flask, render_template

set_cwd()
from src.events import socketio
from src.routes import main



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(main)

    socketio.init_app(app)

    return app