ASC = 'asc'
DESC = 'desc'

class ColumnURL(object):
    """
    Represents the url a column's data should point to.

    :params

    url - The reversible namespace / name combination for the
            relevant view

    args - A LIST of arguments to pass (even if there's just one),
            all of which correspond to model fields

    attrs - A DICT of arguments to set as the anchor tag attributes, NOT
            including the href (of course)

    Ex:
        class MyColumnUrl(ColumnURL):
            url = 'namespace:name'
            args = ['field1', 'field2']
            attr = {'class': 'btn btn-primary'}
    """
    url = None
    args = []
    attrs = None


class Column(object):
    """
    Generic table column based off object access.  Built to work with models.

    :params

    csv_value -- Return the value to write to a csv file

    field - The field to use for this column

    header - What to display in the <th></th> tag

    accessor - How to get the data, with respect to the parent
                object.  For example, if I have a field 'created'
                and I only want to display the date, I could set
                the annotation to 'created.date'.  This is also
                where you would utilize related fields, for
                example, 'participant__full_name'

    annotation - An annotation that needs to be added to the
                queryset before the value is accessed.  This
                takes the form of a callable, so a lambda or
                function reference is appropriate here.

    default - What to display if the data is NULL.

    css_class - A class name to apply to each TD in the table.

    url_class - The ColumnURL class for the field.

    key - Not set by the user.  Basically, whatever we name the
            column in the table class.  This is used to help
            both determine the field and header if either are
            not explicitly set in the constructor.  For example,
            a column declared ``field = Column()`` will have
            a field ``field`` and a header ``Field`` as neither
            were explicitly set

    editable - Whether the column should render a field from a supplied
            formset.

    sortable - Whether or not the field should be sortable. The lookup chain
            for the sorting field is `sort_field` -> `accessor` -> `field`,
            so a custom accessor is followed if applicable

    sort_field - An optional field to pass that should map directly to the
            field name that the django ORM expects, if you're making use of
            some special case accessor to do rendering.
    """
    def __init__(self, field=None, header=None, accessor=None,
                 annotation=None, default=None, css_class=None,
                 url_class=None, editable=False, sortable=False,
                 sort_field=None):
        self.field = field
        self.header = header
        self.accessor = accessor
        self.annotation = annotation
        self.default = '---' if default is None else default
        self.css_class = css_class
        self.url_class = url_class
        self.key = None
        self.editable = editable
        self.sortable = sortable
        self.sort_field = sort_field

    def is_linked(self):
        return self.url_class is not None

    def get_url(self, request=None):
        return self.url_class()

    def csv_value(self, object):
        return Column.value(self, object)

    def value(self, object):
        if self.accessor is None and '__' not in self.field:
            # accessor is just a plain field
            object = getattr(object, self.field)
        elif hasattr(self.accessor, '__call__'):
            # accessor can be a callable
            object = self.accessor(object)
        else:
            # accessor is some crazy dot or underscore notation
            chain = self.accessor or self.field
            arg = chain.replace('__', '.').split('.')
            for a in arg:
                if object is None:
                    return self.default
                fn = getattr(object, a)
                object = fn() if callable(fn) else fn
        return object or self.default

    def get_sort_field(self):
        return self.sort_field or self.accessor or self.field

    def render_sort(self, direction):
        return (self.render_sort_asc() if direction == ASC
                else self.render_sort_desc())

    def render_sort_asc(self):
        return self.get_sort_field()

    def render_sort_desc(self):
        return '-%s' % self.render_sort_asc()


class DictColumn(Column):
    """
    Dict Column for tables based off REST objects and other dictionaries.

    This is meant to be used in conjunction with MockQuerySet found in utils.py
    """
    def value(self, d):
        if self.accessor is None and '__' not in self.field:
            # accessor is just a plain field
            d = d.get(self.field, None)
        elif hasattr(self.accessor, '__call__'):
            # accessor can be a callable
            d = self.accessor(d)
        else:
            # accessor is some crazy dot or underscore notation
            chain = self.accessor or self.field
            arg = chain.replace('__', '.').split('.')
            for a in arg:
                if d is None:
                    return self.default
                fn = d.get(a, None)
                d = fn() if callable(fn) else fn
        return d or self.default


class FieldColumn(Column):
    def __init__(self, *args, **kwargs):
        raise Exception("FieldColumn is no longer used."
                        " Use Column(editable=True)")
