import json
import re
from functools import update_wrapper

from django.http import QueryDict, HttpResponseRedirect
from django.utils.decorators import classonlymethod
from django.utils.safestring import mark_safe
from django.views.generic.list import (MultipleObjectTemplateResponseMixin,
                                       BaseListView)
from django.http import HttpResponse

from inspect import getmembers

from .forms import EditTableSubmitForm
from .paginator import NamespacedPaginator, MockPage
from django.core.paginator import EmptyPage
from .table import Table


class TablesMixin(object):

    """
    Mixin to generate a set of tables for a view.

    This mixin expects a self.queryset variable to exist.
    Thus, it must be added to a ListView or a child class of ListView

    Each table you want needs to be declared as a class attribute, as
    such:

        class MyView(TablesMixin, ListView):
            main_table = MyCrazyTable()

    When you want to render the table, the generic template
    general/table.html expects a context variable called table.
    Therefore, you should utilize a with statement in your template
    for proper rendering, something like:

        {% with tables.my_table as table %}
            {% include "general/table.html %}
        {% endwith %}

    """

    def dispatch(self, *args, **kwargs):
        self.table_pages = {}

        if kwargs.pop('__as_csv', False):
            return self.csv(*args, **kwargs)

        return super(TablesMixin, self).dispatch(*args, **kwargs)

    @classonlymethod
    def as_csv(cls, **initkwargs):
        def csv_view(request, *args, **kwargs):
            kwargs['__as_csv'] = True
            self = cls(**initkwargs)
            self.request = request
            self.args = args
            self.kwargs = kwargs

            return self.dispatch(request, *args, **kwargs)

        update_wrapper(csv_view, cls, updated=())
        update_wrapper(csv_view, cls.dispatch, assigned=())
        return csv_view

    def csv(self, *args, **kwargs):
        """
        CSV Renderer for a table view. Exports the view contents as a CSV
        using the same internals as a standard view.
        """

        table_key = self.request.GET.get('namespace', 'main_table')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = (
            'attachment; filename=%s' % self.get_csv_filename(table_key))

        writer = csv.writer(response)
        table = self.get_table(table_key)
        writer.writerow(table.headers())

        filtered_qs = table.filter(self.get_table_qs(table_key).all())
        qs = table.annotate(filtered_qs)

        for obj in qs:
            writer.writerow(self.prepare_obj_for_csv(table, obj))

        return response

    def get_csv_filename(self, table_key=None):
        return '%s-export.csv' % (table_key or 'table')

    def prepare_obj_for_csv(self, table, obj):
        cols = []
        for key in table.table_sequence:
            value = table.table_columns[key].csv_value(obj)
            cols.append(value.encode('utf8', 'ignore')
                        if isinstance(value, unicode) else value)
        return cols

    def get_table_keys(self):
        return [k for k, v in getmembers(self) if isinstance(v, Table)]

    def get_table(self, table_key):
        return getattr(self, table_key, None)

    def get_current_page(self, table_key):
        return self.request.GET.get('%s-page' % table_key, 1)

    def get_current_sort(self, table_key):
        return self.request.GET.get('%s-sort' % table_key, None)

    def get_page_data(self, table_key):
        if table_key not in self.table_pages.keys():

            table = self.get_table(table_key)
            filtered_qs = table.filter(self.get_table_qs(table_key).all())
            sorted_qs = table.sort(
                filtered_qs,
                self.get_current_sort(table_key))

            qs = table.annotate(sorted_qs)
            p = self.get_current_page(table_key)
            if table.is_paged:
                paginator = NamespacedPaginator(
                    qs, table.table_page_limit, namespace=table_key,
                    current_page=p)
                try:
                    page = paginator.page(p)
                except EmptyPage:
                    page = paginator.page(paginator.num_pages)
            else:
                page = MockPage(qs)

            self.table_pages[table_key] = page

        return self.table_pages[table_key]

    def get_context_data(self, **kwargs):

        ctx = super(TablesMixin, self).get_context_data(**kwargs)

        # Class Dict shortcut
        table_keys = self.get_table_keys()
        tables = {}
        # Note, l(k) is the table in context
        for k in table_keys:
            table = dict()
            table['namespace'] = k
            table['table'] = self.get_table(k)
            table['page_obj'] = self.get_page_data(k)
            table['applied_sort'] = self.get_current_sort(k)
            tables.update({k: table})

        ctx.update({'tables': tables})
        return ctx

    def get_table_qs(self, table_key=None, **kwargs):
        """
        get_table_qs fetches the table queryset.  Passed in this function is
        the table key, which can either be ignored or utilized to differentiate
        between tables, in cases where multiple models are being used.

        This is done because there are instances where filter will not suffice,
        especially in cases where GET and POST parameters or URL kwargs are
        used to decide what to display, as opposed to passing all of that info
        around.
        """
        return self.get_queryset().all()


class EditTablesMixin(TablesMixin):

    """
    Enhance the base Tables Mixin to work with formsets and modelforms in
    order to do bulk editing on entire tables full of data.

    This is to be used in place of the TablesMixin where required, not in
    conjuntion with it.
    """

    def get_context_data(self, **kwargs):
        """
        Enhance the table context data with the generated formsets
            { "main_table": {
                "table": <Table Object>,
                "formset": <EddittableTable Formset Object>,
                "...": ...
            }

        Optionally pass in formsets as a keyword argument to pass in your
        own formset (i.e. when it contains validation errors, etc)
        """
        ctx = super(EditTablesMixin, self).get_context_data(**kwargs)

        formsets = kwargs.pop('formsets', self.get_formsets())

        for k, tbl_entry in ctx['tables'].items():
            tbl_entry['formset'] = formsets[k]
            tbl_entry['submit_form'] = EditTableSubmitForm(
                table=self.get_table(k), table_key=k)
        return ctx

    def get_formsets(self):
        """
        Take a page from the FormView's get_form method, but to work
        with multiple formsets on a given page.

        Is used to both build, and bind the forms within the formset.
        """
        fs = {}

        for k in self.get_table_keys():
            table = self.get_table(k)
            qs = self.get_page_data(k).object_list

            # Avoid ValidationErrors by not attempting to construct FormSets
            # with no data.
            # TODO: Generate some kind of feedback for an empty submission
            if qs and self.request.method == 'POST':
                fs[k] = table.FormSet(self.request.POST, prefix=k)
            else:
                fs[k] = table.FormSet(queryset=qs, prefix=k)
        return fs

    def post(self, request, *args, **kwargs):
        """
        Handle POSTs in a similar way to the FormView does.

        For best UX, it does a complete pass over to validate the entire
        formset for the submitting table, and if it does not validate, it
        will go through the individual records and save the forms for the
        ones who do.
        """
        # artifact of subclassing BaseListView up the chain.
        self.object_list = self.get_queryset()

        formsets = self.get_formsets()
        valid = True
        for formset in formsets.values():
            if formset.is_valid():
                formset.save()
            else:
                # save any correct ones.
                valid = False
                [form.save() for form in formset.forms if form.is_valid()]

        return self.form_valid() if valid else self.form_invalid(formsets)

    def form_valid(self):
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, formsets):
        return self.render_to_response(
            self.get_context_data(object_list=self.object_list,
                                  formsets=formsets))


class FilteredListView(MultipleObjectTemplateResponseMixin, BaseListView):

    """
    Adds a filtering form to the standard ListView. The filtering parameters
    may also be (optionally) added to the context (e.g. to maintain
    filter settings when using pagination links).

    Depends on the django_filters app.
    """
    filter_class = None
    propagate_filter_params = False

    _filter_form = None
    _filter_keys = None

    def get_queryset(self):
        """
        If `filter_class` is unspecified, the queryset will be returned
        unfiltered.
        """
        qs = super(FilteredListView, self).get_queryset()

        if self.filter_class:
            # Filter the query set
            f = self.filter_class(self.request.GET, queryset=qs)
            self._filter_form = f.form
            self._filter_keys = f.filters.keys()
            qs = f.qs

        return qs

    def get_context_data(self, **kwargs):
        context = super(FilteredListView, self).get_context_data(**kwargs)
        context['filter_form'] = self._filter_form
        if self.propagate_filter_params:
            # Add the (URL encoded) filter parameters
            context['filter_params'] = self._get_filter_params()
        return context

    def filter_key(self, key):
        """
        This function allows for the proper propagation
        of get variables from ranged filter fields.
        """
        p = re.compile("^(.*)_\d+$")
        m = p.match(key)
        return m.group(1) if m is not None else key

    def _get_filter_params(self):
        filter_params = QueryDict('').copy()

        for k in self.request.GET.keys():
            if self.filter_key(k) in self._filter_keys:
                filter_params.setlist(k, self.request.GET.getlist(k))

        return filter_params.urlencode()
