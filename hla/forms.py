from django import forms
from hla.models import ImportData, Results, Tests


class UploadDataForm(forms.Form):
    file = forms.FileField()