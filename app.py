from flask import Flask
from config import inject_dependencies

def create_app():
    app = Flask(__name__)
    inject_dependencies(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()