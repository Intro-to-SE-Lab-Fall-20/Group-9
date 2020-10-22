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
    sec_prot = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return f"User('{self.email}', '{self.password}', '{self.imap_server}', '{self.smtp_server}', '{self.smtp_port}')"

class Emails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120), nullable=False)   # email of receiver
    sender = db.Column(db.String(120), nullable=False) # email of sender
    subject = db.Column(db.String(360), nullable=True)
    date_received = db.Column(db.String(360), nullable=False)
    body = db.Column(db.String())
    body_is_html = db.Column(db.Boolean())

    def __repr__(self):
        return f"Email('{self.user}', '{self.sender}', '{self.subject}', '{self.date_received}')"
