import logging
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Div, Submit

logger = logging.getLogger("sheepdog_tables")


class CSVExportForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput)


class EditTableSubmitForm(forms.Form):

    def __init__(self, table, table_key, *args, **kwargs):
        self.table = table
        if not any([c.editable for c in self.table.table_columns.values()]):
            print "Warning: Editable table has no editable columns"
        super(EditTableSubmitForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                HTML("<h4>Bulk Editing</h4>"),
                HTML("<p>This will submit all fields in the table.</p>"),
                Div(
                    Div(
                        Submit(
                            name='submit', value="Save",
                            data_edittable_form="edittable_%s" % table_key,
                            css_class="btn btn-primary"),
                        css_class="filter-btns btn-group"),
                    css_class="filter-btns-row btn-toolbar"),
                css_class="well filtering-well"),
        )
