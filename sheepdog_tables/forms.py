from django import forms

class CSVExportForm(forms.Form):
    """
    Simple CSV Export form with minimal required fields.

    :param id: A Hidden CharField to hold a list of ids to export
    """
    id = forms.CharField(widget=forms.HiddenInput)
