class ColumnURL(object):
    """
    Represents the url a column's data should point to.

    :param url: The reversible namespace / name combination for the relevant view
    :param args: A list of arguments to pass (even if there's just one), all of which correspond to model fields
    :param attrs: A dict of arguments to set as the anchor tag attributes, NOT including the href (of course)

    Example:

    ::

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

    :param field: Object field for reference.  Either this or accessor must be set.
    :param header: A verbose title for this column.
    :param accessor: Access path to data. Ex. 'created.date' or 'user__username'
    :param annotation: A callable for data annotation, if needed.
    :param default: What to display if the data is NULL.
    :param url_class: The :py:class:`ColumnURL` class for the field.

    """
    def __init__(self, field=None, header=None, accessor=None,
                annotation=None, default=None, url_class=None):
        self.field = field
        self.header = header
        self.accessor = accessor
        self.annotation = annotation
        self.default = default or '---'
        self.url_class = url_class
        self.key = None

    def is_linked(self):
        """
        Whether this column has an associated :py:class:`ColumnURL` class.
        
        :returns: True or False based off mentioned criteria.
        """
        return self.url_class is not None

    def get_url(self, request=None):
        """
        Helper method for :py:class:`ColumnURL` object.

        :param request: The HTTP request in context.  Used in method overloading.
        :returns: A new instance of the :py:class:`ColumnURL` class for this column.
        """
        return self.url_class()

    def csv_value(self, object):
        """
        Overloadable function for CSV export

        :param object: The current model object in context
        :returns: The designated value for a CSV file
        """
        return Column.value(self, object)

    def value(self, object):
        """
        Accesses an object's value at a given column or returns default.

        :param object: The current model object in context
        :returns: The appropriate value or default.
        """
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


class DictColumn(Column):
    """
    Dict Column for tables based off REST objects and other dictionaries.
    This is meant to be used in conjunction with :py:class:`MockQuerySet` found in
    :py:mod:`utils`
    """
    def value(self, d):
        """
        Accesses a dictionary's value at a given colum or returns default.
        
        :param d: The dictionary for the row in context.
        :returns: The appropriate value or default.
        """
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
