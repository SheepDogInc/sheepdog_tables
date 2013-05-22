from inspect import getmembers
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from sheepdog_tables.column import Column

class Table(object):
    """
    Generic table base class

    This is for adding model based tables to your page.  It doesn't
    need to know what model it is using, it's all based off whatever
    queryset the ListView class contains (see docs for _`TablesMixin`)

    Each column is set as a normal class attribute.  For instance:

    ::

        class MyCrazyTable(Table):
            field1 = Column()
            second = Column(field="field2", header="Hello")


    :param table_page_limit: The number of items to show per page.
    :param table_attrs: HTML Attributes for <table></table> tags
    :param table_empty: String to print if no data is available
    :param table_sequence: The explicit sequence of columns to show. Required.

    :param is_paged: Defines whether the table should be paged.
    """
    table_page_limit = getattr(settings, 'DEFAULT_ITEMS_PER_PAGE', 25)
    table_attrs = {'class': 'table table-bordered table-striped'}
    table_empty = _("No data is available")
    table_sequence = []

    def __init__(self, is_paged=True):
        if not self.table_sequence:
            raise ImproperlyConfigured('%s does not provide a table_sequence.' % self.__class__.__name__)
        self.table_columns = {}
        self.is_paged = is_paged
        self.gen_columns()

    def gen_columns(self):
        """
        Populate {self.table_columns} with each table column object, keyed by
        attribute name.  Also sets the field attribute on each column to the
        attribute name unless it was manually set by the programmer.
        """
        members_dict = dict(getmembers(self))
        l = lambda k: members_dict[k]
        # Extract the columns into our own nifty dict for later
        for k in members_dict.keys():
            if isinstance(l(k), Column):
                # Field becomes the key value if it isn't passed
                # to the column explicitly
                if not l(k).field:
                    l(k).field = k
                self.table_columns[k] = l(k)

    def filter(self, queryset):
        """
        Entry point for custom filtering.

        :param queryset: to filter
        :returns: The filtered QuerySet
        """
        return queryset

    def annotate(self, queryset):
        """
        Performs the grunt work of annotating a queryset per column which
        defines an annotation.

        :param queryset: The QuerySet to annotate
        :returns: The Annotated QuerySet
        """
        cols = self.table_columns
        annotated_columns = [col for col in cols
                             if cols[col].annotation is not None]

        for col in annotated_columns:
            queryset = cols[col].annotation(queryset)

        return queryset

    def headers(self):
        """
        Get a list of headers for this table

        :returns: the list of headers
        """
        return [self.table_columns[h].header or h.title()
                for h in self.table_sequence]
