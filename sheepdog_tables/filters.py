from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Submit
import django_filters
from django.core.exceptions import FieldError
from django.forms.fields import ChoiceField
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from django_filters.filters import ChoiceFilter


class BaseFilterSet(django_filters.FilterSet):

    """
    This is the base filterset for our widget.

    :params

        filter_sequence - Explicit ordered list of filters to add.

    """

    filter_sequence = []

    @property
    def form(self):
        form = super(BaseFilterSet, self).form

        if not hasattr(form, 'helper'):
            form.helper = FormHelper()
            form.helper.form_method = 'GET'
            form.helper.form_class = 'form'
            form.helper.layout = Layout(
                Div(
                    Div(
                        Div(
                            HTML("<h4>%s</h4>" % ugettext('Filtering')),
                            Div(css_class="filter-table"),
                            css_class="filter-container"),
                        Div(
                            Div(
                                HTML('<div class="filter-selector '
                                     'btn-group"></div>'),
                                HTML('<a href="javascript:void(0)" '
                                     'class="btn filter-buttons btn-reset"'
                                     '>%s</a>' % ugettext('Reset')),
                                Submit(
                                    name='submit', value=ugettext('Apply'),
                                    css_class='btn btn-primary '
                                              ' filter-buttons'),
                                css_class="filter-btns btn-group"
                            ),
                            css_class="filter-btns-row btn-toolbar",
                        ),
                        Div(
                            *tuple([f for f in self.filter_sequence]),
                            css_class='filter-fields'),
                        css_class="well filtering-well"),
                    css_class='')
            )
        return form
