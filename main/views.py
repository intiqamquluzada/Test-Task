from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import MyUser as User
from .forms import InstagramAddForm
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def profile(request, slug):
    user = get_object_or_404(User, slug=slug)
    user.instagram.followers = scrape_data(request)['followers']
    user.instagram.following = scrape_data(request)['following']
    context = {
        'user': user,
        'insta_datas': scrape_data(request)
    }
    return render(request, "profile.html", context)


def add_instagram(request, slug):
    user = get_object_or_404(User, slug=slug)

    context = {}
    form = InstagramAddForm()
    if request.method == "POST":
        form = InstagramAddForm(request.POST or None)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = user
            new_account.save()
            return redirect("main:home", slug=user.slug)
        else:
            print(form.errors)
            form = InstagramAddForm()

    context['form'] = form

    return render(request, "instagram-add.html", context)


def scrape_data(request):
    username = request.user.instagram.username
    password = request.user.instagram.password
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
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
    return new_dict

