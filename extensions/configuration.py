from cryptography.fernet import Fernet
from dynaconf import FlaskDynaconf
from importlib import import_module
import os

def init_app(app):
    FlaskDynaconf(app)

def load_credentials(app):
    f = Fernet(os.environ['CREDENTIALS_KEY'].encode("utf-8"))
    for credential in ['SQLALCHEMY_DATABASE_URI', 'MAIL_USERNAME', 'MAIL_PASSWORD']:
        app.config[credential] = f.decrypt(app.config[credential].encode("utf-8")).decode("utf-8")

def load_modules(app):
    for module in app.config['MODULES']:
        module_name, factory = module.split(':')
        imported = import_module(module_name)
        if (factory):
            getattr(imported, factory)(app)