from . import views
from django.urls import path


app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("activate/<slug>/", views.activate_user_view, name="activate"),
]