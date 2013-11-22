__version__ = '1.2.0'

try:
    from django.conf import settings
    getattr(settings, 'dummy_attr', 'dummy_value')
    _LOAD_PACKAGES = True
except:
    # Just running sdist, we think
    _LOAD_PACKAGES = False

if _LOAD_PACKAGES:
    from mixins import TablesMixin, EditTablesMixin, FilteredListView
    from column import ColumnURL, Column, DictColumn, FieldColumn
    from table import Table, EditTable
