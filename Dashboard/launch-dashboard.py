from g9dashboard import app as dashboard_app
import webbrowser
import threading

if __name__ == '__main__':

    url = 'http://127.0.0.1:8080/'

    threading.Timer(1, lambda: webbrowser.open_new(url) ).start()

    dashboard_app.run(
        host = '127.0.0.1',
        port = 8080,
        debug=False
    )
