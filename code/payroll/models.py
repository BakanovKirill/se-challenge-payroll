import os

from django.contrib.auth.models import User
from django.db import models


class JobGroup(models.Model):
    group_type = models.CharField(max_length=1)
    per_hour_amount = models.DecimalField(decimal_places=2, max_digits=12, null=True, blank=True)

    def __str__(self):
        return self.group_type


class Employee(models.Model):
    job_group = models.ForeignKey(JobGroup, on_delete=models.CASCADE)


class Report(models.Model):
    """
    Stores uploaded CSV file and connects DailyData instances
    """
    csv_file = models.FileField(upload_to='reports')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return os.path.basename(self.csv_file.file.name)


class DailyData(models.Model):
    """
    Stores the row of uploaded CSV reports which come as this:
    | date	  hours worked	  employee id	  job group |

    `CSV_TO_DB_FIELDS` is used during parsing to rename fields.

    `job_group` is essential here as `Employee.job_gruop` can be changed and we can't rely
     on that relation when calculating amounts to pay.
    """

    CSV_TO_DB_FIELDS = {
        'date': 'date',
        'hours worked': 'hours_worked',
        'employee id': 'employee',
        'job group': 'job_group',
    }
    date = models.DateField()
    hours_worked = models.DecimalField(decimal_places=2, max_digits=6)

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    job_group = models.ForeignKey(JobGroup, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)


class PayPeriod(models.Model):
    """
    Stores amount paid to Employee per period of time between `start` and `end`.
    PayPeriod is unique for each employee-start-end combination.
    """
    start = models.DateField()
    end = models.DateField()
    amount_paid = models.DecimalField(decimal_places=2, max_digits=12, default=0, blank=True)

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return "Employee (%s): %s - %s" % (self.employee.id, self.start, self.end)

    class Meta:
        unique_together = ['start', 'end', 'employee']
