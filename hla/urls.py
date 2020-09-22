from django.urls import path
from hla import views
from hla.models import ImportData
from .views import HomePageView, SearchResultsView


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("hla/<name>", views.hello_there, name="hello_there"),
    path("import/", views.import_data, name="import"),
    path("search_results/", SearchResultsView.as_view(), name="search_results"),
]

