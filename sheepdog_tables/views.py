import csv
import logging
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import View
from sheepdog_tables.forms import CSVExportForm
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)
logger.warning("sheepdog_tables.views.CSVExportView is deprecated"
               " in favor of sheepdog_tables.views.CSVExportView")


class CSVExportView(View):
    """
    CSVExport View designates a POST method that can be used to output a CSV file
    based on a table given as 'table'.  This should only be posted to, and thus
    should be on it's own URL.

    :params

    filename -- the filename to write to, without an extension

    table -- the table to use as a template

    form_class -- used to render the form on whatever other page you want.

    redirect -- Where to go if the pks value is empty

    Meta.model -- the model we are using
    """

    filename = None
    table = None
    form_class = CSVExportForm
    redirect = None

    class Meta:
        model = None

    @classmethod
    def get_csvexport_form(cls, queryset=None):
        initial = {}
        if queryset:
            initial = {
                'id': ','.join([str(pk['pk']) for pk in queryset.values('pk')])
            }
        return cls.form_class(initial=initial)

    def post(self, request, *args, **kwargs):
        pks = request.POST.get('id', None)

        if self.redirect is None:
            raise ImproperlyConfigured("CSVExportView redirect attribute not "
                                       "set")

        if not pks:
            url = self.redirect() if callable(self.redirect) else self.redirect
            return redirect(url)

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
        cols = []
        for key in self.table.table_sequence:
            value = self.table.table_columns[key].csv_value(obj)
            cols.append(value.encode('utf8', 'ignore') if isinstance(value, unicode) else value)

        writer.writerow(cols)

    def export_objects_to_csv(self, writer, objects):
        for obj in objects:
            self.export_object_to_csv(writer, obj)

    def annotate(self, objects, request=None):
        return objects
