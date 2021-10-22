from flask import render_template

def inject_controller(app):

    @app.route('/', methods=['GET'])
    @app.auth.authentication_required(redir=True)
    def index():
        return render_template('index.html')