import calendar
import collections

from payroll.models import PayPeriod


def get_period_dates(date):
    """
    Makes (1, 15) or (16, <end_of_month>) tuple based on given day and month of `date` object


    :param date: Date instance
    :return: tuple as (start,end) dates
    """
    period_start = 1
    period_end = 15
    if date.day > 15:
        period_start = 16
        # Get last day of month
        period_end = calendar.monthrange(date.year, date.month)[1]
    return date.replace(day=period_start), date.replace(day=period_end)


def compose_pay_periods(dataset):
    """
    Create or update PayPeriod instances for each employee from DailyData
    Adds the amount_paid to the existing PayPeriod.amount_paid in case of update.

    :param dataset: list of DailyData instances
    :return: list of updated PayPeriod instances
    """
    grouped_dataset = collections.defaultdict(list)
    for daily_data in dataset:
        # Need to group the dataset by employee + period dates range.
        period_start, period_end = get_period_dates(daily_data.date)
        period = (period_start, period_end, daily_data.employee)
        # period_data = (period_start, period_end, daily_data.employee)
        grouped_dataset[period].append(daily_data)
    for period_tuple, daily_datas in grouped_dataset.items():
        period, created = PayPeriod.objects.get_or_create(
            start=period_tuple[0],
            end=period_tuple[1],
            employee=period_tuple[2]
        )
        period.amount_paid += sum(
            [daily_data.job_group.per_hour_amount * daily_data.hours_worked for daily_data in daily_datas]
        )
        period.save()


def get_sorted_periods():
    return PayPeriod.objects.values('id', 'employee', 'amount_paid', 'start', 'end').order_by(
        'employee',
        'start'
    )
