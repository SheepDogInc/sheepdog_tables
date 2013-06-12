from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Submit
import django_filters
from django.core.exceptions import FieldError
from django.forms.fields import ChoiceField
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from django_filters.filters import ChoiceFilter


def build_srtby(instance):
    """
    Builds the choice selection for a sort filter.
    Requires a filter named srtby exists.  Initial is the
    name of the field to use
    """
    instance.filters['srtby'].extra.update({
        'choices': [(instance.filters[f].name or f, instance.filters[f].label or f.title())
        for f in instance.filter_sequence]
    })


class SortChoice(object):

    """
    Represents a choice from a SortChoiceFilter.

    :params

    reverse - Whether or not this is reverse order

    value - The field or SORT_ACTION to use
    """
    reverse = False
    value = ""

    def __init__(self, value):
        self.reverse = value[0] == '-'
        self.value = value[1:] if self.reverse else value


def sort_action(queryset, value):
    """
    This sorts using a SortChoice object, which contains value
    and direction information.  Value could be a field or an
    action value as found in SORT_ACTION
    """
    # We're already in order!
    if queryset.ordered or not isinstance(value, SortChoice):
        return queryset

    attr = value.value

    try:
        list(queryset.order_by(value.value))
    except FieldError:
        pass
    else:
        queryset = queryset.order_by(attr)

    return queryset.reverse() if value.reverse else queryset


class SortChoiceField(ChoiceField):

    """
    Cleans the value by making a SortChoice object out of it, and then
    doing normal validation on the choice.value
    """

    sort_default = None

    def __init__(self, *args, **kwargs):
        super(SortChoiceField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if value is None:
            return SortChoice(self.sort_default)

        choice = SortChoice(value)
        choice.value = super(SortChoiceField, self).clean(choice.value)
        return choice


class SortChoiceFilter(ChoiceFilter):
    field_class = SortChoiceField


class BaseSortableFilterSet(django_filters.FilterSet):

    """
    This is the base filterset for our widget.

    :params

    filter_sequence - Explicit ordered list of filters to add.  DO NOT inlcude
    srtby or srton in this list, as they are added elsewhere.

    srtby - Sort By selector

    srton - Sort On selector
    """
    filter_sequence = []

    srtby = SortChoiceFilter(label=_("Sort By"), action=sort_action)
    srton = django_filters.ChoiceFilter(
        label=_("Order"), choices=(('0', '0'), ('1', '1')),
        action=lambda q, v: q)

    def __init__(self, *args, **kwargs):
        super(BaseSortableFilterSet, self).__init__(*args, **kwargs)
        build_srtby(self)

    @property
    def form(self):
        form = super(BaseSortableFilterSet, self).form

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
                        HTML("<h4>%s</h4>" % ugettext("Sorting")),
                        Div(
                            Div('srtby', css_class='span7'),
                            Div('srton', css_class='span5'),
                            css_class="filter-container row-fluid"
                        ),
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
