from flask import render_template, redirect, url_for, request

from engine import rules

def init_app(app):

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            login_success = rules.try_login(email, password)
            if login_success:
                user = rules.get_current_user()
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error='Invalid e-mail or password')
        return render_template('login.html')
    
    @app.route('/logout')
    def logout():
        rules.try_logout()
        return redirect(url_for('index'))