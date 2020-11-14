from flask import render_template

from g9notes import app

@app.route('/')
def homepage():
    return render_template('homepage.html')
