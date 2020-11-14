from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, FileField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from g9client.models import User
import os

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    imap_server = StringField('IMAP Server', validators=[DataRequired()])
    smtp_server = StringField('SMTP Server', validators=[DataRequired()])
    smtp_port = IntegerField('SMTP Port', validators=[DataRequired()])
    sec_prot = SelectField("Security Protocol", choices = [('ssl', 'ssl'), ('tls', 'tls')])

    submit = SubmitField('Register Account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# Submit button for syncing mail
class SyncMailForm(FlaskForm):
    submit = SubmitField("Sync Mail")

class EmailForm(FlaskForm):
    to = StringField('To', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    attachment = FileField('Upload File')

class SearchForm(FlaskForm):
    search = StringField('', validators=[DataRequired()])
    submit = SubmitField('Search')

class ForwardForm(FlaskForm):
    to = StringField('To', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    added_content = TextAreaField('Additional Content', validators=[DataRequired()])
