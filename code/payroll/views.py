from django.template.loader import render_to_string

from annoying.decorators import render_to

from rest_framework import views
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from payroll.serializers import ReportSerializer
from payroll.utils import compose_pay_periods, get_sorted_periods


@render_to('landing.html')
def landing(request):
    return {'pay_periods': get_sorted_periods()}


class FileUploadView(views.APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        ser = ReportSerializer(data={'csv_file': request.FILES.get('file', None)})
        ser.is_valid(raise_exception=True)
        report = ser.save()
        # Generate report data
        compose_pay_periods(report.dailydata_set.select_related('employee', 'job_group'))

        return Response(
            status=200,
            data=render_to_string('period_rows.html', context={'pay_periods': get_sorted_periods()})
        )
