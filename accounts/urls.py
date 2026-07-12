from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login_view"),
    path("profile/", views.profile, name="profile"),
    path("change-password/", views.change_password, name="change_password"),
    path("refresh/", views.refresh_token, name="refresh token"),
    path("logout/", views.logout, name="logout")
]
