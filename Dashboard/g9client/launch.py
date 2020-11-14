from g9client import app as email_app
import webbrowser
import threading

if __name__ == '__main__':
    url = 'http://0.0.0.0:8084/'
    threading.Timer(1, lambda: webbrowser.open_new(url) ).start()
    email_app.config.update(SESSION_COOKIE_NAME="email-client")
    email_app.run(host = '0.0.0.0', port = 8084, debug=False)
