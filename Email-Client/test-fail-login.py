import time
from selenium import webdriver
from multiprocessing import Process

from g9client import app

test_email = "fail@email.com"
test_password = "1234"

server = Process(
    target=app.run,
    kwargs = {
        "host":"127.0.0.1",
        "port":8080,
        "debug":False
    }
)
server.start()

time.sleep(3) # Give time for server to start

# selenium part
driver = webdriver.Chrome("/usr/local/share/chromedriver")

driver.get('http://127.0.0.1:8080/')

driver.find_element_by_id("email").send_keys(test_email)

driver.find_element_by_id("password").send_keys(test_password)

driver.find_element_by_id("submit").click()

error_message = driver.find_element_by_class_name("alert").text
assert "Login unsuccessful. Please check email and password." in error_message

driver.quit() # Close the webdriver

server.terminate() # Terminate the flask app
server.join()
