# Generated by Django 2.1.2 on 2018-11-06 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DailyData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('hours_worked', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='JobGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_type', models.CharField(max_length=1)),
                ('per_hour_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PayPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('amount_paid', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csv_file', models.FileField(upload_to='reports')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='job_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.JobGroup'),
        ),
        migrations.AddField(
            model_name='dailydata',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.Employee'),
        ),
        migrations.AddField(
            model_name='dailydata',
            name='job_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.JobGroup'),
        ),
        migrations.AddField(
            model_name='dailydata',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.Report'),
        ),
        migrations.AlterUniqueTogether(
            name='payperiod',
            unique_together={('start', 'end', 'employee')},
        ),
    ]