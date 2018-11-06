import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.conf import settings
from django.urls import reverse

from payroll import validation_messages
from payroll.utils import get_period_dates
from payroll.models import DailyData, Employee, Report, PayPeriod, JobGroup


class TestPayRoll(TestCase):
    fixtures = ['admin.json', 'groups.json']

    def test_fixtures_are_fine(self):
        self.assertEquals(User.objects.count(), 1)
        admin = User.objects.first()
        self.assertEquals(admin.username, 'admin')
        self.assertEquals(JobGroup.objects.count(), 2)
        self.assertTrue(JobGroup.objects.filter(group_type='A').exists())
        self.assertTrue(JobGroup.objects.filter(group_type='B').exists())

    def test_get_period_dates(self):
        first_part_date = datetime.date(2018, 11, 5)
        start, end = get_period_dates(first_part_date)
        self.assertEquals(start.day, 1)
        self.assertEquals(end.day, 15)
        second_part_date = datetime.date(2018, 11, 25)
        start, end = get_period_dates(second_part_date)
        self.assertEquals(start.day, 16)
        self.assertEquals(end.day, 30)

    def test_upload_flow(self):
        """
        sample_test.csv:

            date,      hours worked, employee id, job group
            14/11/2016,     7.5,      1,           A
            9/11/2016,      4,        2,           B
            10/11/2016,     4,        2,           B
            8/11/2016,      6,        3,           A
            report id,1,,

        :return:
        """
        client = Client()
        # Test wrong extension file
        with open('%s/manage.py' % settings.BASE_DIR) as wrong_format_file:
            result = client.post(reverse('upload_report'), {'file': wrong_format_file})
            self.assertEquals(result.status_code, 400)
            json = result.json()
            self.assertIn('csv_file', json.keys())
            self.assertEquals(json['csv_file'], [validation_messages.FILE_HAS_WRONG_FORMAT])
        # Test correct file
        with open("%s/sample_test.csv" % settings.BASE_DIR) as csv_file:
            result = client.post(reverse('upload_report'), {'file': csv_file})
            self.assertEquals(result.status_code, 200)
            self.assertEquals(Employee.objects.count(), 3)
            self.assertEquals(DailyData.objects.count(), 4)
            self.assertEquals(PayPeriod.objects.count(), 3)
            self.assertIn('p_1', result.data)
            self.assertIn('p_3', result.data)
            p_1 = PayPeriod.objects.filter(employee=1).first()
            self.assertIsNotNone(p_1)
            self.assertEquals(p_1.amount_paid, 7.5 * 20)  # 'A' group 20$ per hour
            self.assertEquals(p_1.start, datetime.date(2016, 11, 1))
            self.assertEquals(p_1.end, datetime.date(2016, 11, 15))
        # Test same report twice.
        with open("%s/sample_test.csv" % settings.BASE_DIR) as csv_file:
            result = client.post(reverse('upload_report'), {'file': csv_file})
            self.assertEquals(result.status_code, 400)
            json = result.json()
            self.assertIn('csv_file', json.keys())
            self.assertEquals(json['csv_file'], [validation_messages.REPORT_ALREADY_EXISTS])
