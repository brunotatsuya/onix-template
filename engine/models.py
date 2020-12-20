from extensions.database import db
from flask_login import UserMixin
    
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(512))       

    def __init__(self, email, password):
        self.email = email
        self.password = password