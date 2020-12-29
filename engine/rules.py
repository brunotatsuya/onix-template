from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user

from extensions.database import db
from extensions.authentication import lm
from extensions.mail import m

from engine.models import User

### User Authentication Rules

def create_user(email, password):
    if User.query.filter_by(email=email).first():
        raise RuntimeError(f'{email} already registered')
    user = User(email, generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return user

def verify_account(email):
    return User.query.filter_by(email=email).first()
    
def try_send_reset_password(email):
    return m.send_mail('Reset your password', [email], 'This is an test email')

def try_login(email, password):
    if not email or not password:
        return False
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    if (user.password == password):
        login_user(user)
        return True
    return False

@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

def get_current_user():
    return current_user

def try_logout():
    if(current_user.is_authenticated):
        logout_user()
    return True