import csv
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import View
from sheepdog_tables.forms import CSVExportForm
from django.core.exceptions import ImproperlyConfigured

class CSVExportView(View):
    """
    CSVExport View designates a POST method that can be used to output a CSV file
    based on a table given as 'table'.  This should only be posted to, and thus
    should be on it's own URL.

    :param filename: The filename to write to, without an extension
    :param table: The table to use as a template
    :param form_class: Used to render the form on whatever other page you want.
    :param redirect: Where to go if the pks value is empty
    """

    filename = None
    table = None
    form_class = CSVExportForm
    redirect = None

    class Meta:
        """
        :param model: The Model we are using
        """
        model = None

    @classmethod
    def get_csvexport_form(cls, queryset=None):
        """
        Generates a :py:class:`CSVExportForm`

        :param queryset: The queryset to use for form initialization
        """
        initial = {}
        if queryset:
            initial = {'id': ','.join([pk['pk'] for pk in queryset.values('pk')])}
        return cls.form_class(initial=initial)

    def post(self, request, *args, **kwargs):
        """
        HTTP POST Handler for Form Data.  Does CSV Export.

        :param request: The request in context.
        :return: Response with CSV file or redirect on error
        """
        pks = request.POST.get('id', None)

        if self.redirect is None:
            raise ImproperlyConfigured("CSVExportView Redirect Attribute not set")

        if pks is None:
            return redirect(self.redirect)

        pks = pks.split(',')

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % self.filename

        writer = csv.writer(response)

        objects = self.Meta.model.objects.filter(pk__in=pks)
        objects = self.table.filter(objects)
        objects = self.annotate(objects, request)

        writer.writerow(self.table.headers())
        self.export_objects_to_csv(writer, objects)

        return response

    def export_object_to_csv(self, writer, obj):
        """
        Worker function for building CSV and proper character encoding.

        :param writer: The CSV writer we are utilizing.
        :param obj: The current model object in context.
        """
        cols = []
        for key in self.table.table_sequence:
            value = self.table.table_columns[key].csv_value(obj)
            cols.append(value.encode('utf8', 'ignore') if isinstance(value, unicode) else value)

        writer.writerow(cols)

    def export_objects_to_csv(self, writer, objects):
        """
        Worker function to scroll through and process objects.

        :param writer: The CSV writer we are utilizing
        :param objects: The list of objects we are including in output.
        """
        for obj in objects:
            self.export_object_to_csv(writer, obj)

    def annotate(self, objects, request=None):
        """
        Overridable annotation function for extra required data.

        :param objects: The list of objects to act on.
        :param request: The current request in context.
        :return: The passed objects.
        """
        return objects
