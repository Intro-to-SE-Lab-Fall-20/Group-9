from flask import render_template, url_for, flash, redirect, request
from g9client import app, db, bcrypt
from g9client.forms import RegistrationForm, LoginForm, SyncMailForm, EmailForm, SearchForm
from g9client.models import User, Emails
from g9client.functions import syncMail
from flask_login import login_user, current_user, logout_user, login_required
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
    #paginate account page to give user more control of movement between many emails -> paginate(page=page, per_page=5)
    #sort in descending order to view newest emails first -> order_by(Email.date_recieved.desc())
    page = request.args.get('page', 1, type=int)
    emails = Emails.query.filter_by(user=current_user.email).order_by(Emails.date_received.desc()).paginate(page=page, per_page=5)

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
    # if form.validate_on_submit():
    #     post = Post(title=form.title.data, content=form.content.data, author=current_user)
    #     db.session.add(post)
    #     db.session.commit()
    #     flash('Your email has been created!', 'success')
    #     return redirect(url_for('home'))
    return render_template('create-email.html', title='Compose Message', form=form, legend='Compose Message')

#route for search functionality
@app.route('/search', methods=['GET', 'POST'])
def search():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('search.html', form=search)
#route for results from search
@app.route('/results')
def search_results(search):
    results = search.data['search']
    emails = Emails.query.filter_by(user=current_user.email).all()
    count = 0
    for email in emails:
        if results == email.subject or results == email.sender or results == email.date_recieved or results == email.body:
            count = count + 1
    if count > 0:
        #display results on full page (this can be changed to have certain amount on pages with "per_page=#")
        page = request.args.get('page', 1, type=int)
        emails = Emails.query.order_by(Emails.date_received.desc()).paginate(page=page)
        return render_template('results.html', emails=emails, results=results)
    else:
        flash('No results found!', 'danger')
        return redirect('/search')
        