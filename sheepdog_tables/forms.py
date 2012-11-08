from django import forms

class CSVExportForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput)
