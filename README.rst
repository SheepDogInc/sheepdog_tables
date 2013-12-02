Sheepdog Tables API
===================

This API helps with quick and easy table creation. It allows for
displaying of model data, arbitrary data, annotated data, and the like.
It also allows for simple CSV exporting via a CSV export view.

The codebase is well documented, and each class should have a relevant
docstring.


Installation
------------

Install the python package using pip

.. code:: bash

    $ pip install sheepdog-tables

Install javascript dependencies

Example Bower configuration with supported versions of javascript dependencies. 

.. code:: javascript

    {
        "name": "my_project",
        "version": "0.0.0",
        "dependencies": {
            "bootstrap": "3.0.1",
            "backbone": "1.0.0",
            "underscore": "1.4.4"
        }
    }
            

JS is written in coffeescript, and we suggest using a project like
django-compressor to compress your static files and compile the coffeescript on
your behalf.

.. code:: bash

    $ pip install django-compressor==1.3

.. code:: html

    <script type="text/javascript" src="{% static "bower/jquery/jquery.min.js" %}"></script>
    <script type="text/javascript" src="{% static "tables/js/jquery.ba-bbq.js" %}"></script>

    <!-- To enable filtering -->
    <script type="text/javascript" src="{% static "bower/underscore/underscore.js" %}"></script>
    <script type="text/javascript" src="{% static "bower/backbone/backbone.js" %}"></script>
    <script type="text/coffeescript" src="{% static "tables/js/filtering.coffee" %}"></script>

    <!-- Event binding for sorting, pagination, etc. -->
    <script type="text/coffeescript" src="{% static "tables/js/binding.coffee" %}"></script>


Starting Points
---------------

A few things should be noted for this API. The primary mixin to add a
table to a page is ``TablesMixin``. The corresponding template is found
in ``tables/tables.html``. The mixin should be mixed in to a class based
view inheriting from a ``ListView``. It's ``get_context_data`` method
should be run after the ListView's same function.

Each table is to be declared as class parameters. For example, if I have
two tables, ``Table1`` and ``Table2``, we could have a class that looks
like this:

.. code:: python


    class MyView(TablesMixin, ListView):
        table_1 = Table1()
        table_2 = Table2()

        def get_context_data(self, **kwargs):
            context = ListView.get_context_data(self, **kwargs)
            context.update(TablesMixin.get_context_data(self, **kwargs)


The table class works similarly to models. Full docs for that are in
it's class doc string.

Good practice with this API
---------------------------

The general rules of Django and Python apply to the application of this
API. Generally, it is a good idea to have all of your tables for your
application in a tables.py file, and columns in their own separate
columns.py file, just like one would do for forms and fields.
