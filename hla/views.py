import re
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from hla.forms import LogMessageForm, AddResult, AddTest
from hla.models import ImportData, Results, Tests, Locus, Patients
from django.views.generic import ListView, TemplateView

class HomePageView(ListView):
    '''Renders home page.'''
    model = Results
    template_name = 'hla/home.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        query_as_id = Patients.objects.get(patientNumber=query).patientID
        object_list = Results.objects.filter(patientID=query_as_id)
        return object_list


def import_data(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "hla/import_data.html", {"form": form})

