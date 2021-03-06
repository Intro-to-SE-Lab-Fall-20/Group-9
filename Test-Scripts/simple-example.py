import time
from selenium import webdriver
from multiprocessing import Process
import sys

sys.path.append("Group-9/Email-Client")

from g9client import app

server = Process(
    target=app.run,
    kwargs = {
        "host":"127.0.0.1",
        "port":8080,
        "debug":False
    }
)
server.start()

# selenium part
driver = webdriver.Chrome()

driver.get('http://127.0.0.1:8080/');
time.sleep(1)

driver.quit() # Close the webdriver

server.terminate() # Terminate the flask app
server.join()
