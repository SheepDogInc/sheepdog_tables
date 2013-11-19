__version__ = '1.0.6'

try:
    from django.conf import settings
    getattr(settings, 'dummy_attr', 'dummy_value')
    _LOAD_PACKAGES = True
except:
    # Just running sdist, we think
    _LOAD_PACKAGES = False

if _LOAD_PACKAGES:
    from mixins import (TablesMixin, EditTablesMixin, FilteredListView,
                        SortFilterMixin, CSVTableMixin)
    from column import ColumnURL, Column, DictColumn, FieldColumn
    from filters import (SortChoice, SortChoiceField, SortChoiceFilter,
                         BaseSortableFilterSet)
    from table import Table, EditTable
