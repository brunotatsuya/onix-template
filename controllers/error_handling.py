from flask import render_template, redirect, url_for

def inject_controller(app):

    @app.errorhandler(404)
    @app.route('/404', methods=['GET'])
    @app.auth.authentication_required(redir=True)
    def handler_404(e=None):
        return render_template('404.html')
    
    @app.errorhandler(500)
    @app.route('/500', methods=['GET'])
    @app.auth.authentication_required(redir=True)
    def handler_500(e=None):
        return render_template('500.html')