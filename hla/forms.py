from django import forms


class UploadDataForm(forms.Form):
    file = forms.FileField()