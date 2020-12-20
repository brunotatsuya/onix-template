from dynaconf import FlaskDynaconf
from importlib import import_module

def init_app(app):
    FlaskDynaconf(app)

def load_modules(app):
    for module in app.config['MODULES']:
        module_name, factory = module.split(':')
        imported = import_module(module_name)
        if (factory):
            getattr(imported, factory)(app)
