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


class SearchResultsView(ListView):
    """Renders list of search results."""
    model = Results
    template_name = 'hla/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        query_as_id = Patients.objects.get(patientNumber=query).patientID
        object_list = Results.objects.filter(patientID=query_as_id)
        return object_list


def search_results(request):
    return render(request, "hla/search_results.html")

def about(request):
    return render(request, "hla/about.html")

def contact(request):
    return render(request, "hla/contact.html")

def hello_there(request, name):
    return render(
        request,
        'hla/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

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

def addResult(request):
    form = AddResult(request.POST or None)
    if form.is_valid():
        result = form.save(commit=False)
        result.log_date = datetime.now()
        result.save()
        result_instance = Results.objects.create(testID='1', result='12:13', alleleID='2')
        render(request, 'addResult.html.html')
        return redirect("home")

def addTest(request):
    form = AddTest(request.POST or None)
    if form.is_valid():
        test = form.save(commit=False)
        test.log_date = datetime.now()
        test.save()
        return redirect("home")

def myView(request):
    query_results = Results.object.all()
