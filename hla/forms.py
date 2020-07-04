from django import forms
from hla.models import ImportData

class LogMessageForm(forms.ModelForm):
    class Meta:
        model = ImportData
        fields = ("message",)   # NOTE: the trailing comma is required