import time
from selenium import webdriver
from multiprocessing import Process

from g9client import app

test_user_email = "test@email.com"
test_user_password = "admin2020"
test_user_imap = "imap.email.com"
test_user_smtp = "smtp.email.com"
test_user_port = 465

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
time.sleep(1)

driver.find_element_by_id("register_link").click()
time.sleep(1)

driver.find_element_by_id("email").send_keys(test_user_email)

driver.find_element_by_id("password").send_keys(test_user_password)

driver.find_element_by_id("imap_server").send_keys(test_user_imap)

driver.find_element_by_id("smtp_server").send_keys(test_user_smtp)

driver.find_element_by_id("smtp_port").send_keys(test_user_port)

driver.find_element_by_id("submit").click()
time.sleep(3)

popup_message = driver.find_element_by_class_name("alert").text
assert "Account details registered for test@email.com!" in popup_message

driver.find_element_by_id("email").send_keys(test_user_email)

driver.find_element_by_id("password").send_keys(test_user_password)

driver.find_element_by_id("submit").click()
time.sleep(3)

assert driver.current_url == 'http://127.0.0.1:8080/account'

driver.quit() # Close the webdriver

server.terminate() # Terminate the flask app
server.join()
