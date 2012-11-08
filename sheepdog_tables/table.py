from inspect import getmembers
from django.core.exceptions import ImproperlyConfigured
from .column import Column
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

class Table(object):
    """
    Generic table base class

    This is for adding model based tables to your page.  It doesn't
    need to know what model it is using, it's all based off whatever
    queryset the ListView class contains (see docs for ``TablesMixin``)

    Each column is set as a normal class attribute.  For instance:

        class MyCrazyTable(Table):
            field1 = Column()
            second = Column(field="field2", header="Hello")


    :params

    table_page_limit - The number of items to show per page.

    table_attrs - HTML Attributes for <table></table> tags

    table_empty - String to print if no data is available

    table_sequence - The explicit sequence of columns to show.
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
        # l(k) -> class.__dict__[k]
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
        return queryset

    def annotate(self, queryset):
        cols = self.table_columns
        annotated_columns = [col for col in cols
                             if cols[col].annotation is not None]

        for col in annotated_columns:
            queryset = cols[col].annotation(queryset)

        return queryset

    def headers(self):
        return [self.table_columns[h].header or h.title()
                for h in self.table_sequence]
