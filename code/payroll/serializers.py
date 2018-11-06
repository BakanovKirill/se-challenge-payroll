import csv
from decimal import Decimal
from io import TextIOWrapper

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField

from payroll.models import Report, DailyData, Employee, JobGroup, PayPeriod


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['csv_file']

    def validate_csv_file(self, value):
        if value.content_type != 'text/csv':
            raise ValidationError({'file': _('The file must be in CSV format.')})
        return value

    def create(self, validated_data):
        """
        1. Before creating, adds additional validation on existing Report.
        2. Adds DailyData instances from CSV file after report is created.

        (1) also can be done in validate() method but this means we have to read the file twice.

        :param validated_data:
        :return:
        """
        with validated_data['csv_file'].open() as csv_file:
            csv_file = TextIOWrapper(csv_file.file, encoding='utf-8')
            content = csv_file.readlines()
            last_line_n = len(content) - 1
            footer = content[last_line_n]
            report_id = footer.split('report id,')[1].split(',')[0]
            # Validate existing report id.
            if Report.objects.filter(id=report_id).exists():
                raise ValidationError({'csv_file': 'This report already exists. Upload another file.'})

            validated_data['id'] = report_id
            # Preload job groups into dict so we have group_type:id pairs
            groups_by_type = {group['group_type']: group['id'] for group in JobGroup.objects.values('id', 'group_type')}
            with transaction.atomic():
                report = super().create(validated_data)
                # Parse the CSV and create related DailyData instances
                data_list = []
                csv_reader = csv.DictReader(content[:last_line_n], delimiter=',', quotechar='|')
                for row in csv_reader:
                    ready_data = {'report': report.id}
                    for key in row.keys():
                        # Transition csv column names to db field names
                        ready_data[DailyData.CSV_TO_DB_FIELDS[key]] = row[key]
                    ready_data['job_group'] = groups_by_type[ready_data['job_group']]
                    ready_data['employee'] = {'id': ready_data['employee'], 'job_group': ready_data['job_group']}

                    data_list.append(ready_data)
                dd_serializer = DailyDataSerializer(data=data_list, many=True)
                dd_serializer.is_valid(raise_exception=True)
                dd_serializer.save()
                return report


class EmployeeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False)

    class Meta:
        model = Employee
        fields = ('id', 'job_group')

    def create(self, validated_data):
        instance = super().create(validated_data)
        return instance


class DailyDataSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()

    class Meta:
        model = DailyData
        fields = '__all__'

    def create(self, validated_data):
        employee = validated_data.pop('employee')
        # Create employee or update the job group.
        employee, created = Employee.objects.update_or_create(
            id=employee['id'],
            defaults={'job_group': employee['job_group']}
        )
        validated_data['employee'] = employee
        instance = super().create(validated_data)
        return instance


class PayPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayPeriod
        fields = '__all__'
