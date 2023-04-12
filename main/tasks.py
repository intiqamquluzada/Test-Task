from celery import shared_task
from requests import request
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from .models import Instagram
from django.core.exceptions import ObjectDoesNotExist
import pickle



chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.binary_location = "/usr/bin/chromium-browser"
chrome_options.add_argument("--remote-debugging-port=9222")
driver = webdriver.Chrome(
    executable_path="/usr/bin/chromedriver",
    chrome_options=chrome_options
)


@shared_task
def scrape_data(request):
    username = request.user.instagram.username
    password = request.user.instagram.password

    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(2)
    username_field = driver.find_element(By.NAME, 'username')
    username_field.send_keys(username)
    password_field = driver.find_element(By.NAME, 'password')
    password_field.send_keys(password)
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button.click()
    WebDriverWait(driver, 10).until(EC.url_contains('instagram.com'))
    driver.maximize_window()

    # Add a delay before navigating to the profile page
    time.sleep(10)

    # Navigate to the profile page
    profile_url = f"https://www.instagram.com/{username}/"
    driver.get(profile_url)

    # Wait for the login process to complete
    time.sleep(10)
    ul = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'ul')))
    items = ul.find_elements(By.TAG_NAME, 'li')
    my_dict = []
    for item in items:
        print(item.text)
        my_dict.append(item.text)
    new_dict = {s.split()[1]: int(s.split()[0]) for s in my_dict}
    try:
        instagram = request.user.instagram
    except ObjectDoesNotExist:
        instagram = Instagram(user=request.user)
    instagram.followers = new_dict['followers']
    instagram.following = new_dict['following']
    instagram.save()



