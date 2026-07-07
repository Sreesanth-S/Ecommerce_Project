from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login_view"),
    path("profile/", views.profile, name="profile"),
    path("refresh/", views.refresh_token, name="refresh token")
]
