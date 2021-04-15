import time
import datetime
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User

from .forms import *
from .models import *


def time_post1(request, cookie, the_action):
    try:
        date_time1 = request.COOKIES[cookie]
    except KeyError:
        date_time1 = None
    if date_time1:
        choice = request.POST.get('action')
        if choice.find(the_action) != -1:
            date_time1 = datetime.datetime.strptime(date_time1, '%B %d, %Y, %I:%M:%S %p')
            t1 = int(date_time1.timestamp())
            now = datetime.datetime.now()
            t2 = int(now.timestamp())
            t3 = t2 - t1
            return t3
        else:
            t3 = 0
            return t3
    else:
        t3 = 0
        return t3


def time_post(request, cookie):
    try:
        date_time = request.COOKIES[cookie]
    except KeyError:
        date_time = None
    if date_time:
        date_time = datetime.datetime.strptime(date_time, '%B %d, %Y, %I:%M:%S %p')
        t1 = int(date_time.timestamp())
        now = datetime.datetime.now()
        t2 = int(now.timestamp())
        t3 = t2 - t1
        return t3
    else:
        t3 = 0
        return t3


def enable_button():
    button = str(list(Action.objects.all())[-1])
    if button.find('plan') != -1:
        result = '#plan'
        return result
    elif button.find('setup') != -1:
        result = '#setup'
        return result
    elif button.find('auto_serv') != -1:
        result = '#auto_serv'
        return result
    elif button.find('ppr') != -1:
        result = '#ppr'
        return result
    elif button.find('breaking') != -1:
        result = '#breaking'
        return result
    elif button.find('material') != -1:
        result = '#material'
        return result
    elif button.find('task') != -1:
        result = '#task'
        return result
    elif button.find('model') != -1:
        result = '#model'
        return result


def action(request):
    if 'date_time' in request.COOKIES and 'date_time1' in request.COOKIES:
        act = request.POST.get('action1')
    else:
        act = request.POST.get('action')
    return act


def checkout(request, message, message1):
    if 'date_time' and 'date_time1' in request.COOKIES:
        messages.add_message(request, messages.INFO, message)
        return True
    elif 'date_time' in request.COOKIES:
        messages.add_message(request, messages.INFO, message1)
        return True
    else:
        return False


def machine_choice(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except TypeError:
        employee = None
    except Employee.DoesNotExist:
        employee = None
    try:
        employee_machine = list(EmployeeMachine.objects.filter(employee=employee.pk))[-1]
        choice = Machine.objects.filter(employeemachine=employee_machine)[0]
    except IndexError:
        choice = ''
    except AttributeError:
        choice = ''
    if not choice:
        choice = 'unselected'
    return choice


class Main(View):

    def get(self, request):
        if request.is_ajax() and \
                Employee.objects.filter(user__exact=request.user.pk).count() and \
                EmployeeMachine.objects.filter(employee=Employee.objects.get(user=request.user).pk):
            date_time = request.GET.get('button_text')
            date_time1 = request.GET.get('new_button_text')
            if date_time:
                if 'date_time' in request.COOKIES:
                    response = HttpResponse()
                    response.delete_cookie("date_time")
                    return response
                else:
                    response = HttpResponse()
                    response.set_cookie("date_time", date_time)
                    return response
            if date_time1:
                if 'date_time1' in request.COOKIES:
                    response = HttpResponse()
                    response.delete_cookie("date_time1")
                    return response
                else:
                    response = HttpResponse()
                    response.set_cookie("date_time1", date_time1)
                    return response
            if "date_time" in request.COOKIES and 'date_time1' in request.COOKIES:
                return JsonResponse({
                    'seconds': request.COOKIES['date_time'],
                    'seconds1': request.COOKIES['date_time1'],
                    'button_choice': enable_button()
                }, status=200)
            elif "date_time" in request.COOKIES:
                return JsonResponse({
                    'seconds': request.COOKIES['date_time'],
                    'button_choice': enable_button()
                }, status=200)
        if request.user.is_authenticated:
            context = {
                'nav_bar': 'home',
                'machine': machine_choice(request)
            }
            return render(request, 'mainapp/main.html', context=context)
        else:
            return redirect('/login/')

    def post(self, request):
        if request.is_ajax() and \
                Employee.objects.filter(user__exact=request.user.pk).count() and \
                EmployeeMachine.objects.filter(employee=Employee.objects.get(user=request.user).pk):
            data = {
                'secs': datetime.datetime.strftime(datetime.datetime.now(), "%S"),
                'minutes': datetime.datetime.strftime(datetime.datetime.now(), "%M"),
                'hour': datetime.datetime.strftime(datetime.datetime.now(), "%H"),
                'day': datetime.datetime.strftime(datetime.datetime.now(), "%d"),
                'month': datetime.datetime.strftime(datetime.datetime.now(), "%m"),
                'year': datetime.datetime.strftime(datetime.datetime.now(), "%Y")
            }
            bound_form = TimeForm(data=data)
            if bound_form.is_valid():
                bound_form.save()
                data1 = {
                    'name': action(request),
                    'emp_mach': list(EmployeeMachine.objects.filter(employee=Employee.objects.get(user=1).pk))[-1],
                    'time': list(Time.objects.all())[-1],
                    'total': time_post(request, 'date_time'),
                    'plan': time_post1(request, 'date_time1', 'plan'),
                    'setup': time_post1(request, 'date_time1', 'setup'),
                    'auto_serv': time_post1(request, 'date_time1', 'auto_serv'),
                    'ppr': time_post1(request, 'date_time1', 'ppr'),
                    'br': time_post1(request, 'date_time1', 'br'),
                    'material': time_post1(request, 'date_time1', 'material'),
                    'task': time_post1(request, 'date_time1', 'task'),
                    'model': time_post1(request, 'date_time1', 'model')
                }
                bound_form1 = ActionForm(data=data1)
                if bound_form1.is_valid():
                    bound_form1.save()
                    return redirect('/')
        else:
            if not Employee.objects.filter(user__exact=request.user.pk).count():
                return redirect('/create-employee/')
            elif not EmployeeMachine.objects.filter(employee=Employee.objects.get(user=request.user).pk):
                return redirect('/employee-machine-binding/')
            else:
                return redirect('/')


class PersonalArea(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        username = request.user
        context = {
            'username': username,
            'nav_bar': 'user',
            'machine': machine_choice(request)
        }
        return render(request, 'mainapp/personal_area.html', context=context)

    def post(self, request):
        if checkout(
                request,
                'Cannot logout until all the counters are turned off',
                'Cannot logout until the main counter is turned off',
        ):
            return redirect('/personal-area/')
        else:
            logout(request)
            return redirect('/login/')


class EmployeeMachineBindingView(View):

    def get(self, request):
        employee = Employee.objects.get(user=request.user)
        data = {
            'employee': employee,
            'machine': machine_choice(request)
        }
        form = EmployeeMachineForm(data=data)
        context = {
            'form': form,
            'employee': employee,
            'nav_bar': 'machine',
            'machine': machine_choice(request)
        }
        return render(request, 'mainapp/employee_machine_binding.html', context=context)

    def post(self, request):
        if not 'date_time' in request.COOKIES:
            bound_form = EmployeeMachineForm(request.POST)
            context = {
                'form': bound_form,
                'nav_bar': 'new_user'
            }
            if bound_form.is_valid():
                bound_form.save()
                return redirect('/')
            return render(request, 'mainapp/employee_machine_binding.html', context=context)
        else:
            messages.add_message(request, messages.INFO,
                                 'Cannot change the machine during the shift')
            return redirect('/employee-machine-binding/')


class CreateAnEmployee(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        user = request.user
        data = {
            'user': user,
            'first_name': user,
            'last_name': 'Ivanov',
            'position': 'workman'
        }
        form = CreateAnEmployeeForm(data=data)
        context = {
            'form': form,
            'nav_bar': 'new_user',
            'machine': machine_choice(request)
        }
        return render(request, 'mainapp/create_employee.html', context=context)

    def post(self, request):
        if not Employee.objects.filter(user__exact=request.user.pk).count():
            bound_form = CreateAnEmployeeForm(request.POST)
            context = {
                'form': bound_form,
                'nav_bar': 'new_user'
            }
            if bound_form.is_valid():
                bound_form.save()
                return redirect('/employee-machine-binding/')
            return render(request, 'mainapp/create_employee.html', context=context)
        else:
            messages.add_message(request, messages.INFO, 'You\'ve already created an employee')
            return redirect('/create-employee/')


class CreateAnUser(View):

    def get(self, request):
        form = CreateAnUserForm()
        context = {
            'anon': request.user.is_anonymous,
            'form': form,
            'nav_bar': 'new_user',
            'machine': machine_choice(request)
        }
        return render(request, 'mainapp/create_user.html', context=context)

    def post(self, request):
        bound_form = CreateAnUserForm(request.POST)
        context = {
            'anon': request.user.is_anonymous,
            'form': bound_form,
            'nav_bar': 'new_user'
        }
        if bound_form.is_valid():
            bound_form.save()
            if request.user.is_anonymous:
                username = request.POST['username']
                password = request.POST['password2']
                user = authenticate(request, username=username, password=password)
                login(request, user)
                return redirect('/create-employee/')
            else:
                messages.add_message(request, messages.INFO, 'User created successfully')
                return redirect('/create-user/')
        return render(request, 'mainapp/create_user.html', context=context)


class Login(View):

    def get(self, request):
        if request.user.is_anonymous:
            form = LoginForm()
            context = {
                'machine': machine_choice(request),
                'anon': request.user.is_anonymous,
                'form': form,
                'nav_bar': 'login'
            }
            return render(request, 'mainapp/login.html', context=context)
        else:
            messages.add_message(request, messages.INFO, 'You need to logout first')
            return redirect('/personal-area/')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            name = User.objects.get(username=username)
        except User.DoesNotExist:
            name = ''
        if not name:
            messages.add_message(request, messages.INFO, 'User with the username isn\'t exist')
            return redirect('/login/')
        try:
            login(request, user)
            return redirect('/')
        except AttributeError:
            messages.add_message(request, messages.INFO, 'Incorrect password')
            return redirect('/login/')
