from datetime import datetime
from g9client import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    imap_server = db.Column(db.String(60), nullable=False)
    smtp_server = db.Column(db.String(60), nullable=False)
    smtp_port = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"User('{self.email}', '{self.password}', '{self.imap_server}', '{self.smtp_server}', '{self.smtp_port}')"
