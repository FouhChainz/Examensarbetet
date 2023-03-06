from django import forms

class SalesUploadForm(forms.Form):
    file = forms.FileField()
