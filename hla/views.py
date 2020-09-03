import re
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from hla.forms import LogMessageForm, AddResult, AddTest
from hla.models import ImportData, Results, Tests
from django.views.generic import ListView

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = Results

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

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
