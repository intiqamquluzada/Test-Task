from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import MyUser as User
from .forms import InstagramAddForm
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def profile(request, slug):
    user = get_object_or_404(User, slug=slug)
    scrape_data(request, user.slug)
    context = {
        'user': user
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


def scrape_data(request, slug):
    user = get_object_or_404(User, slug=slug)
    username = user.instagram.username
    password = user.instagram.password
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(2)
    username_field = driver.find_element(By.NAME, 'username')
    username_field.send_keys(username)
    password_field = driver.find_element(By.NAME, 'password')
    password_field.send_keys(password)
    login_button = driver.find_element_by_css_selector('button[type="submit"]')
    login_button.click()

    # Wait for the login process to complete
    time.sleep(10)
    # insta_url = 'https://www.instagram.com/'
    # driver.get(insta_url + username)
    # following_count = driver.find_element_by_xpath("//a[@href='/{}/following/']/span".format(username))
    # follower_count = driver.find_element_by_xpath("//a[@href='/{}/followers/']/span".format(username))


