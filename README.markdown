# Sheepdog Tables API

This API helps with quick and easy table creation.  It allows for
displaying of model data, arbitrary data, annotated data, and the like.  It also
allows for simple CSV exporting via a CSV export view.

The codebase is well documented, and each class should have a relevant
docstring.

## Starting Points

A few things should be noted for this API.  The primary mixin to add a table to
a page is ```TablesMixin```.  The corresponding template is found in
```tables/tables.html```.  The mixin should be mixed in to a class based view
inheriting from a ```ListView```.  It's ```get_context_data``` method should be 
run after the ListView's same function.

Each table is to be declared as class parameters.  For example, if I have two
tables, ```Table1``` and ```Table2```, we could have a class that looks like
this:

```python

class MyView(TablesMixin, ListView):
    table_1 = Table1()
    table_2 = Table2()

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context.update(TablesMixin.get_context_data(self, **kwargs)

```

The table class works similarly to models.  Full docs for that are in it's class
doc string.

## Good practice with this API

The general rules of Django and Python apply to the application of this API.
Generally, it is a good idea to have all of your tables for your application in
a tables.py file, and columns in their own separate columns.py file, just like
one would do for forms and fields.
