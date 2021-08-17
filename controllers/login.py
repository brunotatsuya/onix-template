from flask import render_template, redirect, url_for

def inject_controller(app):

    @app.route('/login', methods=['GET'])
    def login():
        if app.auth.is_authenticated():
            return redirect(url_for('index'))
        return render_template('login.html')