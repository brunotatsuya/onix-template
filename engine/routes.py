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
    
    @app.route('/reset', methods=['GET', 'POST'])
    def reset():
        if request.method == 'POST':
            email = request.form['email']
            account_exists = rules.verify_account(email)
            if account_exists:
                sent_reset_password = rules.try_send_reset_password(email)
                if sent_reset_password:
                    return render_template('reset.html', message=f'An e-mail was sent to {email}. Please, verifiy your mailbox.')
                else:
                    return render_template('reset.html', error=f'An error has ocurred while sending e-mail to {email}. Please, try again later.')
            else:
                return render_template('reset.html', error=f'The specified e-mail "{email}" is not registered.')
        return render_template('reset.html')

    @app.route('/logout')
    def logout():
        rules.try_logout()
        return redirect(url_for('index'))