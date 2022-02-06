import os
import json
from importlib import import_module

def inject_dependencies(app):
    inject_meta(app)
    inject_configurations(app)
    inject_services(app)
    inject_models(app)
    inject_controllers(app)

def inject_meta(app):
    def model_decorator(name):
        def model_wrapper(class_ref):
            setattr(app, name, class_ref)
            return class_ref
        return model_wrapper
    def service_decorator(name):
        def service_wrapper(class_ref):
            setattr(app, name, class_ref())
            return class_ref
        return service_wrapper
    app.model = model_decorator
    app.service = service_decorator

def inject_configurations(app):
    file_settings = open('settings.json',)
    SETTINGS = json.load(file_settings)
    file_settings.close()
    env = os.environ.get('FLASK_ENV')
    CONFIG = SETTINGS['COMMON_CONFIG']
    if env == 'development':
        CONFIG.update(SETTINGS['DEVELOPMENT_CONFIG'])
    elif env == 'production':
        CONFIG.update(SETTINGS['PRODUCTION_CONFIG'])
    else:
        CONFIG.update(SETTINGS['LOCAL_CONFIG'])
    app.config_dict = CONFIG
    app.secret_key = app.config_dict['SECRET_KEY']

def inject_modules(app, package, common_function):
    dirname = os.path.dirname(__file__)
    services_path = os.path.join(dirname, package.replace('.', '\\'))
    modules = [f"{package}.{m.split('.py')[0]}" for m in os.listdir(services_path) if m.endswith('.py')]
    for module in modules:
        imported = import_module(module)
        getattr(imported, common_function)(app)

def inject_services(app):
    inject_modules(app, 'services', 'inject_service')

def inject_models(app):
    inject_modules(app, 'models', 'inject_model')

def inject_controllers(app):
    inject_modules(app, 'controllers', 'inject_controller')
    inject_modules(app, 'controllers.api', 'inject_controller')