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


def timer2(value='start'):
    t = 0
    while value == 'start':
        t += 1
        time.sleep(1)


def logout_view(request):
    logout(request)
    if "date_time" in request.COOKIES:
        response = HttpResponse("", status=302)
        response['Location'] = '/login/'
        response.delete_cookie("date_time")
        return response
    else:
        return redirect('/login/')


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
        bound_form = EmployeeMachineForm(request.POST)
        context = {
            'form': bound_form,
            'nav_bar': 'new_user'
        }
        if bound_form.is_valid():
            bound_form.save()
            return redirect('/')
        return render(request, 'mainapp/employee_machine_binding.html', context=context)


class Main(View):

    def get(self, request):
        if request.is_ajax():
            if Employee.objects.filter(user__exact=request.user.pk).count() and \
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
                        'seconds1': request.COOKIES['date_time1']
                    }, status=200)
                elif "date_time" in request.COOKIES:
                    return JsonResponse({'seconds': request.COOKIES['date_time']}, status=200)
            else:
                return redirect('/create-employee/')
        if request.user.is_authenticated:
            context = {
                'nav_bar': 'home',
                'machine': machine_choice(request)
            }
            return render(request, 'mainapp/main.html', context=context)
        else:
            return redirect('/login/')

    def post(self, request):
        if Employee.objects.filter(user__exact=request.user.pk).count():
            if EmployeeMachine.objects.filter(employee=Employee.objects.get(user=request.user).pk):
                # timer2() не удаляй, дебил. она тебя сожрёт
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
                        'name': request.POST.get('action'),
                        'emp_mach': list(EmployeeMachine.objects.filter(employee=Employee.objects.get(user=1).pk))[-1],
                        'time': list(Time.objects.all())[-1],
                        'total': 10,
                        'plan': 0,
                        'setup': 0,
                        'auto_serv': 0,
                        'ppr': 0,
                        'br': 0,
                        'material': 0,
                        'task': 0,
                        'model': 0
                    }
                    bound_form1 = ActionForm(data=data1)
                    if bound_form1.is_valid():
                        bound_form1.save()
                        return redirect('/')
                return render(request, 'mainapp/main.html')
            else:
                return redirect('/employee-machine-binding/')
        else:
            return redirect('/create-employee/')


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
            username = request.POST['username']
            password = request.POST['password2']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('/create-employee/')
        return render(request, 'mainapp/create_user.html', context=context)


class Login(View):

    def get(self, request):
        form = LoginForm()
        context = {
            'machine': machine_choice(request),
            'anon': request.user.is_anonymous,
            'form': form,
            'nav_bar': 'login'
        }
        return render(request, 'mainapp/login.html', context=context)

    def post(self, request):
        print('post')
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
