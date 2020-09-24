from django.urls import path
from hla import views
from .views import HomePageView


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("import/", views.import_data, name="import"),
]

