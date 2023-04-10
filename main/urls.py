from django.urls import path
from .views import profile, add_instagram

app_name = 'main'
urlpatterns = [
    path("profile/<slug>/", profile, name='home'),
    path("instagram-add/<slug>/", add_instagram, name='instagram_add'),


]