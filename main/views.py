from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import MyUser as User
from .forms import InstagramAddForm
from .tasks import copy_share_task



def profile(request, slug):
    user = get_object_or_404(User, slug=slug)
    if user.instagram:
        copy_share_task(user.slug)

    user.refresh_from_db()

    context = {
        'user': user,

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
