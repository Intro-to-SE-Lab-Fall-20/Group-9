from flask import render_template, url_for, flash, redirect, request
from g9dashboard import app, db, bcrypt
from g9dashboard.forms import RegistrationForm, LoginForm, LaunchForm
from g9dashboard.models import User
from flask_login import login_user, current_user, logout_user, login_required
import ssl
import os
from g9dashboard.functions import launchClient, launchNotes

@app.route('/', methods=["GET", "POST"])
@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # if user and bcrypt.check_password_hash(user.password, form.password.data):
        if user and user.password == form.password.data: # can't use hashed password; need encryption method
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account details registered for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/home", methods=["GET", "POST"])
@login_required
def home():

    # form = LaunchForm()
    #
    # if form.validate_on_submit():
    #
    #     print("Notes data Value : {value}".format(value=form.notes.data))
    #     print("Client data Value : {value}".format(value=form.client.data))
    #
    #     launchClient()
    #
    #     if form.client.data:
    #         launchClient()
    #     if form.notes.data:
    #         pass


    if request.method == 'POST':
        if request.form.get('Launch Notes'):
            launchNotes()
        elif request.form.get("Launch Email Client"):
            launchClient()

    return render_template('home.html', title='Home')
