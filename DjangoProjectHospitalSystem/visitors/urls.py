from django.urls import path
from . import views

app_name = "visitors"

urlpatterns = [
    path("register/", views.register_visitor, name="register_visitor"),
    path("login/", views.login_visitor, name="login_visitor")

]