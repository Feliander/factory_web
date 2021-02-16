from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)


class Machine(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class EmployeeMachine(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE)

    def __str__(self):
        return 'Employee is ' + str(self.employee) + ' and machine is ' + str(self.machine)


class Time(models.Model):
    secs = models.IntegerField()
    minutes = models.IntegerField()
    hour = models.IntegerField()
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return str(self.day) + '.' + str(self.month) + '.' + str(self.year) + ' ' + str(self.hour) + ':' + str(
            self.minutes) + ':' + str(self.secs)


class Action(models.Model):
    name = models.CharField(max_length=255)
    emp_mach = models.ForeignKey('EmployeeMachine', on_delete=models.CASCADE)
    time = models.ForeignKey('Time', on_delete=models.CASCADE)
    total = models.IntegerField()
    plan = models.IntegerField(blank=True)
    setup = models.IntegerField(blank=True)
    auto_serv = models.IntegerField(blank=True)
    ppr = models.IntegerField(blank=True)
    br = models.IntegerField(blank=True)
    material = models.IntegerField(blank=True)
    task = models.IntegerField(blank=True)
    model = models.IntegerField(blank=True)

    def __str__(self):
        return str(self.name)
