from flask import Flask
from extensions import configuration

def create_app():
    app = Flask(__name__)
    configuration.init_app(app)
    configuration.load_credentials(app)
    configuration.load_modules(app)
    return app