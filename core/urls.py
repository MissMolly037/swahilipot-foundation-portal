from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("settings/logo/", views.logo_settings, name="logo_settings"),
]
