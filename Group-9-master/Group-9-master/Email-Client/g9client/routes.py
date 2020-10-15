from flask import render_template, url_for, flash, redirect, request
from g9client import app, db, bcrypt
from g9client.forms import RegistrationForm, LoginForm, SyncMailForm, EmailForm
from g9client.models import User, Emails
from g9client.functions import syncMail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

import os

@app.route('/', methods=["GET", "POST"])
@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if user and bcrypt.check_password_hash(user.password, form.password.data):
        if user and user.password == form.password.data: # can't use hashed password; need encryption method
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            email=form.email.data,
            password=form.password.data,
            imap_server=form.imap_server.data,
            smtp_server=form.smtp_server.data,
            smtp_port=form.smtp_port.data
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account details registered for {form.email.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    sync = SyncMailForm()
    emails = Emails.query.filter_by(user=current_user.email).all()

    if sync.validate_on_submit(): # Sync new emails
        syncMail(current_user.email, current_user.password , current_user.imap_server)
        flash(f'Inbox updated.', 'success')
        return redirect(url_for('account'))

    return render_template('account.html', title='Account', sync = sync, emails = emails, new_email = new_email)

@app.route('/post/<int:email_id>')
@login_required
def read_email(email_id):
    email = Emails.query.get_or_404(email_id)
    return render_template('read-email.html', title=email.subject, email=email)

@app.route('/email/new', methods=['GET', 'POST'])
@login_required
def new_email():
    form = EmailForm()
    if form.validate_on_submit():
    #     post = Post(title=form.title.data, content=form.content.data, author=current_user)
    #     db.session.add(post)
    #     db.session.commit()
        sender = current_user.email
        receivers = [form.to.data]
        message = form.content.data

            
        msg = MIMEMultipart()
        msg['Subject'] = form.subject.data
        msg['From'] = current_user.email
        msg['To'] = form.to.data

        msgText = MIMEText('<p>%s</p>' % (message), 'html')
        msg.attach(msgText)

        if form.attachment.data != '':
            filename = form.attachment.data
            file = MIMEApplication(open(filename, 'rb').read())
            file.add_header('Content-Disposition', 'attachment', form.attachment.data)
            msg.attach(file)
        
        smtpObj = SMTP(host=current_user.smtp_server, port=current_user.smtp_port)
        smtpObj.starttls()
        smtpObj.login(current_user.email, current_user.password)
        smtpObj.sendmail(sender, receivers, msg.as_string())
        

        smtpObj.quit()

        
        flash('Your email has been created!', 'success')
        return redirect(url_for('account'))
    return render_template('create-email.html', title='Compose Message', form=form, legend='Compose')


