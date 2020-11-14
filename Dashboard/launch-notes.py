from g9notes import app
from g9notes.models import Note, Task
from g9notes.api import api
from g9notes import views

import webbrowser
import threading

api.setup()

if __name__ == '__main__':
    Note.create_table(True)
    Task.create_table(True)

    url = 'http://0.0.0.0:8088/'

    threading.Timer(1, lambda: webbrowser.open_new(url) ).start()

    app.run(
        host = '0.0.0.0',
        port = 8088,
        debug=False
    )
