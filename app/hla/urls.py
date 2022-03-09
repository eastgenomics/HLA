from django.urls import path
from hla import views
from .views import HomePageView, dashboard
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r"^dashboard/", dashboard, name="dashboard"),
    path("", dashboard, name="dashboard"),
    path("home/", HomePageView.as_view(), name="home"),
    path("import/", views.import_data, name="import"),
    path("success/", views.success, name="success"),
    path("failure/", views.failure, name="failure"),
    url(r"^accounts/", include("django.contrib.auth.urls")),

]
