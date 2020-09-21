from django import forms
from hla.models import ImportData, Results, Tests


class LogMessageForm(forms.ModelForm):
    class Meta:
        model = ImportData
        fields = ("message",)   # NOTE: the trailing comma is required


class AddTest(forms.ModelForm):
    class Meta:
        model = Tests
        fields = ("testDate", "confirmed",)


class AddResult(forms.ModelForm):
    class Meta:
        model = Results
        fields = ("patientID", "testID", "locusID", "result",)
