from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user

from extensions.database import db
from extensions.authentication import lm

from engine.models import User

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

def create_user(email, password):
    if User.query.filter_by(email=email).first():
        raise RuntimeError(f'{email} already registered')
    user = User(email, generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return user