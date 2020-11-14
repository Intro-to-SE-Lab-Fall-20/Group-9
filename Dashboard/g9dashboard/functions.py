import webbrowser
import os
from g9dashboard import db, app

from g9client import app as email_app
import threading

import subprocess

def launchClient():
    command1 = "cd " + app.config['APP_DIRECTORY'].replace(" ", "\\ ")
    command2 = "python launch-client.py"

    commands = command1 + ";" + command2

    subprocess.Popen(commands, shell = True)

def launchNotes():
    command1 = "cd " + app.config['APP_DIRECTORY'].replace(" ", "\\ ")
    command2 = "python launch-notes.py"

    commands = command1 + ";" + command2

    subprocess.Popen(commands, shell = True)
