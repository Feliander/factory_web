# Generated by Django 3.1.5 on 2021-02-01 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='action',
            old_name='emp_mach_id',
            new_name='emp_mach',
        ),
        migrations.RenameField(
            model_name='action',
            old_name='time_id',
            new_name='time',
        ),
        migrations.RenameField(
            model_name='employeemachine',
            old_name='employee_id',
            new_name='employee',
        ),
        migrations.RenameField(
            model_name='employeemachine',
            old_name='machine_id',
            new_name='machine',
        ),
    ]
