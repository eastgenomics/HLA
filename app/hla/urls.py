from django.urls import path, re_path
from hla import views
from .views import HomePageView, dashboard
from django.conf.urls import include
from django.contrib import admin

urlpatterns = [
    re_path(r"^dashboard/", dashboard, name="dashboard"),
    path("", dashboard, name="dashboard"),
    path("home/", HomePageView.as_view(), name="home"),
    path("import/", views.import_data, name="import"),
    path("success/", views.success, name="success"),
    path("failure/", views.failure, name="failure"),
    re_path(r"^accounts/", include("django.contrib.auth.urls")),

]
