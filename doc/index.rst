.. sheepdog_tables documentation master file, created by
   sphinx-quickstart on Wed May 22 14:41:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to sheepdog_tables's documentation!
===========================================

.. toctree::
   :maxdepth: 2

sheepdog_tables is a powerful but simple library for table and reports
generation.  Table rows can be both based on Django models and lists of dicts,
in order to work with REST APIs like TastyPie. 

Views implementing tables are based off Django's own `ListView`.  We've made it
easy to include tables in any view however, and don't directly give you a table
view.  This way, you can easily incorporate it into preexisting views, make
whatever modifications you wish, and even include multiple tables in the same
view and have custom processing for each.  The mixin is
:py:class:`sheepdog_tables.mixins.TablesMixin`.

Tables are the heart of this application.  Again, like 
:py:class:`sheepdog_tables.mixins.TablesMixin`, there is a single class,
:py:class:`sheepdog_tables.table.Table`, and this offers several convenience
functions for you to modify data output and the like.  A really simple view
implementation looks like this::

    class MyView(sheepdog_tables.mixins.TablesMixin, ListView):

        model = MyModel

        table_1 = Table1()
        table_2 = Table2()

        def get_context_data(self, **kwargs):
            context = ListView.get_context_data(self, **kwargs)
            context.update(TablesMixin.get_context_data(self, **kwargs))

Note here that we're doing some stuff in `get_context_data`. 
:py:class:`sheepdog_tables.mixins.TablesMixin` requires certain things to be
declared and accessible, which you can read more about in it's documentation,
but it doesn't absolutely require you use a list view at all. We recommend it
though, for sanity's sake. Ordering the contexts like this ensures that the
information that :py:class:`sheepdog_tables.mixins.TablesMixin` needs is
available.  Again, the mixin doesn't assume that you even want to call this
context data, and in Python, explicit is always better than implicit.

Let's take a look at tables now.  In our example above, we've declared two
tables, and included them both in this class.  Context data wise, this will give
us two variables, `table_1` and `table_2`, which we can then use as we please in
the Django template itself, though this package does include a `table.html`
template for you to utilize as a generic way to properly print out a table.
It'll even give you a pager if you've set `is_paged=True` in your table's
constructor!

Tables, as you would assume, are made up of columns.  A simple table could look
like so::

    class Table1(sheepdog_tables.table.Table):
        first = sheepdog_tables.column.Column()
        second = sheepdog_tables.column.Column(field="myfield")

What we have here is a small table with two columns.  Given that this is being
used in the first example, let's assume that our model is `MyModel`.  This means
that the first column listed here will access `MyModel.first`, as we haven't
specified a field.  Furthermore, the column's header will be set to 'First'
automatically.  The second column is a little different.  Because we set a
field, we'll access `MyModel.myfield` as opposed to `MyModel.second`.  Also, our
header will be automatically set to 'Myfield'.  This can be overwritten to
whatever we desire by specifiying a `header=` in the constructor.

What if we want to select a related field, or some other piece of data attached
to a field on a given model, like a date off of a `datetime` object?  Well,
`sheepdog_tables` is smart enough to figure this kind of stuff out.  We have an
alternative keyword argument for the :py:class:`sheepdog_tables.column.Column` 
class called `accessor` that we can specify a 'path' for the column's `value`
function to follow and evaluate.  Examples are as such::

    class Table2(sheepdog_tables.table.Table):
        date_created = sheepdog_tables.column.Column(accessor="created.date")
        related_email = sheepdog_tables.column.Column(accessor="user__email")

Look familiar? We know how to parse both '__' and '.', and grab whatever data
you want.  But what about computed data? For this, we can use django's built in
QuerySet annotations. Again, this is an extra keyword on the column class::

    class Table2(sheepdog_tables.table.Table):
        date_created = sheepdog_tables.column.Column(accessor="created.date")
        related_email = sheepdog_tables.column.Column(accessor="user__email")
        n_related = sheepdog_tables.column.Column(
            annotation=lambda q: q.annotate(n_related=Count('related')))

This is of course assuming that you have, say, an M2M relationship on a field
called 'related', or some other aggregatable field.  An important thing to note
here is that we've gone ahead and set the field name on both the Table and
resultant QuerySet to n_related, which, through the nature of this API, will
automatically access this field for you when you go to display the table. The 
lambda function here takes a queryset, performs an annotation, and returns a 
resultant queryset.

All of these tables should be stored in a file in your app's directory called
'tables.py'.  This keeps them all in one convenient location, and makes it
really easy for you to go and reuse tables.  You can also subclass tables, and
everything will just work as you would expect.

"OK, now how do I display these tables..." you may ask.  Well, we've got a nice,
generic template for you to use.  It expects a single variable to exist in
context, that :py:class:`sheepdog_tables.mixins.TablesMixin` is responsible for
generating on the fly.  It's located in
'sheepdog_tables/templates/tables/table.html', and can be easily included in any
template you write by simply using an include tag.  That variable name? 'table'.
"But.. you called them `table_1` and `table_2`...".  Right, that's because there
were more than one, though honestly, we could have called them `pink` and `blue`
had we wanted to.  This is where the power of Django's templating system comes
in.  Simply put, we use a while block in order to label one of these tables as
`table`, and then include the template within that while block::

    {% with table_1 as table %}
        {% include "sheepdog_tables/tables/table.html" %}
    {% endwith %}

    {% with table_2 as table %}
        {% include "sheepdog_tables/tables/table.html" %}
    {% endwith %}

This lets you have as many tables as you want on screen, ordered however you
want, and placed wherever you want!

Stylewise, attributes are declared on the table itself in the class.  Check out
the docs for :py:class:`sheepdog_tables.table.Table` for more information.  Our
library likes bootstrap, and our templates are written with bootstrap2 in mind,
but feel free to hack away and make our templates work with your favourite
framework.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

