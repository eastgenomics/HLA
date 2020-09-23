import re
from datetime import datetime
from django.http import HttpResponse
from django.db.models.base import ObjectDoesNotExist
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
        #query = self.request.GET['q']
        #ruery = self.request.GET['r']
        #suery = self.request.GET['s']
        #tuery = self.request.GET['t']
        if self.request.GET.get('q'):
            try:
                query = self.request.GET.get('q')
                query_as_id = Patients.objects.get(patientNumber=query).patientID
                object_list = Results.objects.filter(patientID=query_as_id)
            except ObjectDoesNotExist:
                return
        elif self.request.GET.get('r'):
            try:
                query = self.request.GET.get('r')
                query_as_id = Locus.objects.get(locusName=query).locusID
                object_list = Results.objects.filter(locusID=query_as_id)
            except ObjectDoesNotExist:
                return
        elif self.request.GET.get('s'):
            try:
                query = self.request.GET.get('s')
                query_as_id = Tests.objects.get(testDate=query).testID
                object_list = Results.objects.filter(patientID=query_as_id)
            except ObjectDoesNotExist:
                return
        elif self.request.GET.get('t'):
            try:
                query = self.request.GET.get('t')
                object_list = Results.objects.filter(result=query)
            except ObjectDoesNotExist:
                return
        else:
            return
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

