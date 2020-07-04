from django.urls import path
from hla import views
from hla.models import ImportData

home_list_view = views.HomeListView.as_view(
    queryset=ImportData.objects.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    context_object_name="message_list",
    template_name="hla/home.html",
)

urlpatterns = [
    path("", home_list_view, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("hla/<name>", views.hello_there, name="hello_there"),
    path("import/", views.import_data, name="import"),
]

