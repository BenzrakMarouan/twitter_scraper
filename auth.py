import pickle
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_to_twitter(driver, email, username, password, cookies_file):
    driver.get("https://twitter.com/login")

    # Enter the email
    email_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "text"))
    )
    email_field.clear()
    email_field.send_keys(email)
    email_field.send_keys(Keys.RETURN)

    # Enter the username
    username_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "text"))
    )
    username_field.clear()
    username_field.send_keys(username)
    username_field.send_keys(Keys.RETURN)

    # Enter the password
    password_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password_field.clear()
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    # Wait for the home page to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='primaryColumn']"))
    )
    
    # Save cookies
    with open(cookies_file, "wb") as f:
        pickle.dump(driver.get_cookies(), f)

def load_cookies(driver, cookies_file):
    if os.path.exists(cookies_file):
        driver.get("https://twitter.com")
        with open(cookies_file, "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.refresh()
