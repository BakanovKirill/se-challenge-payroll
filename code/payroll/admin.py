from django.contrib import admin

from .models import Employee, JobGroup, PayPeriod, Report, DailyData


class DailyDataAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'hours_worked', 'job_group')


class PayPeriodAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start', 'end', 'amount_paid')


# Register your models here.
admin.site.register(Employee)
admin.site.register(JobGroup)
admin.site.register(PayPeriod, PayPeriodAdmin)
admin.site.register(Report)
admin.site.register(DailyData, DailyDataAdmin)
