from flask import render_template

def inject_controller(app):

    @app.route('/', methods=['GET'])
    @app.auth.authentication_required(redir=True)
    def index():
        return render_template('base.html', username=app.auth.get_authenticated_user())