from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class EmployeeMachineForm(forms.ModelForm):
    class Meta:
        model = EmployeeMachine
        fields = ['employee', 'machine']

        widgets = {
            'employee': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeMachineForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class TimeForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = ['secs', 'minutes', 'hour', 'day', 'month', 'year']


class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = ['name', 'emp_mach', 'time', 'total', 'plan', 'setup', 'auto_serv', 'ppr', 'br', 'material', 'task',
                  'model']


class CreateAnEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'position', 'user']

        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'position': forms.TextInput(),
            'user': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(CreateAnEmployeeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CreateAnUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super(CreateAnUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_username(self):
        username = self.cleaned_data['username'].lower()

        if User.objects.filter(username__iexact=username).count():
            raise ValidationError('The first name {} is already taken. I\'m sorry.'.format(username))
        else:
            return self.cleaned_data['username']


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

        widgets = {
            'username': forms.TextInput(),
            'password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class PersonalAreaForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'last_login', 'is_superuser', 'first_name', 'last_name', 'email',
                  'is_staff', 'is_active', 'date_joined']

        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'last_login': forms.HiddenInput(attrs={'class': 'form-control'}),
            'is_superuser': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'is_staff': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.TextInput(attrs={'class': 'form-control'}),
            'date_joined': forms.DateTimeInput(attrs={'class': 'form-control'})
        }
