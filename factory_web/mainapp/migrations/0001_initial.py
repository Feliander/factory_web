# Generated by Django 3.1.5 on 2021-02-01 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secs', models.IntegerField()),
                ('minutes', models.IntegerField()),
                ('hour', models.IntegerField()),
                ('day', models.IntegerField()),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeMachine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.employee')),
                ('machine_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.machine')),
            ],
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('total', models.IntegerField()),
                ('plan', models.IntegerField(blank=True)),
                ('setup', models.IntegerField(blank=True)),
                ('auto_serv', models.IntegerField(blank=True)),
                ('ppr', models.IntegerField(blank=True)),
                ('br', models.IntegerField(blank=True)),
                ('material', models.IntegerField(blank=True)),
                ('task', models.IntegerField(blank=True)),
                ('model', models.IntegerField(blank=True)),
                ('emp_mach_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.employeemachine')),
                ('time_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.time')),
            ],
        ),
    ]