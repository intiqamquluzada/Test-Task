from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout
from .models import MyUser as User


def login_view(request):
    context = {}
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data.get("email"))
            login(request, user)
            return redirect("main:home", slug=user.slug)
        else:
            print(form.errors)
            form = LoginForm()

    context['form'] = form
    return render(request, "login.html", context)


def logout_view(request):
    logout(request)
    return redirect("accounts:login")


def register_view(request):
    context = {}
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST or None)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get("password1"))
            new_user.save()
            return redirect("accounts:login")
        else:
            print(form.errors)
            form = RegisterForm()

    context['form'] = form
    return render(request, "register.html", context)
