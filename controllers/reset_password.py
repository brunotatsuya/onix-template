from flask import render_template, redirect, url_for

def inject_controller(app):

    @app.route('/reset_password', methods=['GET'])
    def reset_password():
        if app.auth.is_authenticated():
            return redirect(url_for('index'))
        return render_template('resetPassword.html')