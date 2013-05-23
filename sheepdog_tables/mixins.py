from inspect import getmembers
from sheepdog_tables.paginator import NamespacedPaginator
from sheepdog_tables.table import Table

class TablesMixin(object):
    """
    Mixin to generate a set of tables for a view.

    This mixin expects a self.queryset variable to exist.
    Thus, it must be added to a ListView or a child class of ListView

    Each table you want needs to be declared as a class attribute, as
    such:

    ::

        class MyView(TablesMixin, ListView):
            main_table = MyCrazyTable()

    When you want to render the table, the generic template
    *general/table.html* expects a context variable called table.
    Therefore, you should utilize a with statement in your template
    for proper rendering, something like:

    ::

        {% with my_table as table %}
            {% include "general/table.html" %}
        {% endwith %}

    """

    def get_context_data(self, **kwargs):
        """
        Builds and returns a dictionary of tables for a given view.
        """
        # Class Dict shortcut
        l = lambda k: getattr(self, k, None)
        table_keys = [k for k,v in getmembers(self) if isinstance(v, Table)]

        tables = {}

        # Note, l(k) is the table in context
        for k in table_keys:
            table = dict()
            table['table'] = l(k)
            filtered_qs = table['table'].filter(self.get_table_qs(k).all())
            qs = table['table'].annotate(filtered_qs)
            p = self.request.GET.get('%s-page' % k, 1)
            if table['table'].is_paged:
                paginator = NamespacedPaginator(qs, l(k).table_page_limit, namespace=k, current_page = p)
                table['page_obj'] = paginator.page(p)
            else:
                table['page_obj'] = {"object_list": qs}
            tables.update({k: table})

        return tables

    def get_table_qs(self, table_key=None, **kwargs):
        """
        Fetches the table queryset.  Passed in this function is
        the table key, which can either be ignored or utilized to differentiate
        between tables, in cases where multiple models are being used.

        This is done because there are instances where filter will not suffice,
        especially in cases where GET and POST parameters or URL kwargs are
        used to decide what to display, as opposed to passing all of that info
        around.

        :param table_key: Used only if overridden by programmer.
        """
        return self.get_queryset().all()
