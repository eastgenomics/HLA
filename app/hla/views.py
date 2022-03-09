from django.db.models.base import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponseRedirect
from hla.forms import UploadDataForm
from hla.models import Results, Patients
from django.views.generic import ListView
from hla.management.commands.seedFromExcel import importData
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(LoginRequiredMixin, ListView):
    '''Renders home page.'''
    model = Results
    template_name = 'hla/home.html'

    def get_queryset(self):
        if self.request.GET.get('q'):
            try:
                query = self.request.GET.get('q')
                queryAsId = Patients.objects.get(patientNumber=query).patientID
                object_list = Results.objects.filter(patientID=queryAsId)
            except ObjectDoesNotExist:
                object_list = Results.objects.none()
        elif self.request.GET.get('r'):
            try:
                query = self.request.GET.get('r')
                object_list = Results.objects.filter(result=query)
            except ObjectDoesNotExist:
                object_list = Results.objects.none()
        else:
            object_list = Results.objects.none()
        return object_list


def dashboard(request):
    return render(request, "hla/dashboard.html")


@login_required
def import_data(request):
    if request.method == "POST":
        form = UploadDataForm(request.POST, request.FILES)
        if form.is_valid():
            if importData(request.FILES['file']) > 0:
                return HttpResponseRedirect('/failure/')
            else:
                return HttpResponseRedirect('/success/')
    else:
        form = UploadDataForm()
    return render(request, "hla/import_data.html", {"form": form})


@login_required
def success(request):
    return render(request, "hla/success.html")


@login_required
def failure(request):
    return render(request, "hla/failure.html")
