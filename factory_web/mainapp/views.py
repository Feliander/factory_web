import time
import datetime
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse


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


class PersonalArea(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        username = request.user
        context = {
            'username': username,
            'nav_bar': 'user'
        }
        return render(request, 'mainapp/personal_area.html', context=context)


# def employee_machine_binding(request):
#     print('111')
#     if request.is_ajax():
#         machine = request.GET.get('machine')
#         print()
#         print(machine)
#         print()
#     data = {
#         'employee': Employee.objects.get(user=request.user),
#         'machine': Machine.objects.filter(name__iexact='laser3030')
#     }
#     print()
#     print(Machine.objects.get(name='TruLaser 3030'))
#     print()
#     form = EmployeeMachineForm(data)
#     if form.is_valid():
#         form.save()
#         print('success')
#         return redirect('/')
#     print('unfortunately')
#     return redirect('/')


# class EmployeeMachineBindingView(View):
#
#     def get(self, request):
#         print('get request')
#         if request.is_ajax():
#             print('request is ajax')
#             machine = request.GET.get('machine')
#             print()
#             print(machine)
#             print()
#             username = request.user
#             employee = Employee.objects.get(user=request.user)
#             context = {
#                 'username': username,
#                 'employee': employee
#             }
#             return render(request, 'mainapp/employee_machine_binding.html', context=context)
#         return redirect('/')
#
#     def post(self, request):
#         data = {
#             'employee': Employee.objects.get(user=request.user),
#             'machine': Machine.objects.filter(name__iexact='laser3030')
#         }
#         # print()
#         # print(Machine.objects.get(name='TruLaser 3030'))
#         # print()
#         form = EmployeeMachineForm(data)
#         if form.is_valid():
#             form.save()
#             print('success')
#             return redirect('/')
#         print('unfortunately')
#         return redirect('/')


class EmployeeMachineBindingView(View):

    def get(self, request):
        username = request.user
        employee = Employee.objects.get(user=request.user)
        machine = Machine.objects.get(name='TruLaser 3030')
        try:
            machine_choice = \
                Machine.objects.filter(employeemachine=EmployeeMachine.objects.filter(employee=employee.pk)[0])[0]
        except IndexError:
            machine_choice = ''
        if not machine_choice:
            machine_choice = 'unselected'
        data = {
            'employee': employee,
            'machine': machine
        }
        form = EmployeeMachineForm(data=data)
        context = {
            'form': form,
            'username': username,
            'employee': employee,
            'nav_bar': 'machine',
            'machine': machine_choice
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
            if Employee.objects.filter(user__exact=request.user.pk).count():
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
            employee = Employee.objects.get(user=request.user)
            try:
                machine_choice = Machine.objects.filter(employeemachine=EmployeeMachine.objects.filter(employee=employee.pk)[0])[0]
            except IndexError:
                machine_choice = ''
            if not machine_choice:
                machine_choice = 'unselected'
            context = {
                'nav_bar': 'home',
                'machine': machine_choice
            }
            return render(request, 'mainapp/main.html', context=context)
        else:
            return redirect('/login/')

    def post(self, request):
        if Employee.objects.filter(user__exact=request.user.pk).count():
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
                return redirect('/')
            return render(request, 'mainapp/main.html')
        else:
            return redirect('/create-employee/')


class CreateAnEmployee(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        if not Employee.objects.filter(user__exact=request.user.pk).count():
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
                'nav_bar': 'new_user'
            }
            return render(request, 'mainapp/create_employee.html', context=context)
        else:
            raise PermissionError('Error')

    def post(self, request):
        bound_form = CreateAnEmployeeForm(request.POST)
        context = {
            'form': bound_form,
            'nav_bar': 'new_user'
        }
        if bound_form.is_valid():
            bound_form.save()
            return redirect('/')
        return render(request, 'mainapp/create_employee.html', context=context)


class CreateAnUser(View):

    def get(self, request):
        form = CreateAnUserForm()
        context = {
            'anon': request.user.is_anonymous,
            'form': form,
            'nav_bar': 'new_user'
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
            return redirect('http://127.0.0.1:8000/create-employee/')
        return render(request, 'mainapp/create_user.html', context=context)


class Login(View):

    def get(self, request):
        try:
            employee = Employee.objects.get(user=request.user)
        except TypeError:
            employee = None
        try:
            machine_choice = \
                Machine.objects.filter(employeemachine=EmployeeMachine.objects.filter(employee=employee.pk)[0])[0]
        except IndexError and AttributeError:
            machine_choice = ''
        if not machine_choice:
            machine_choice = 'unselected'
        form = LoginForm()
        context = {
            'machine': machine_choice,
            'anon': request.user.is_anonymous,
            'form': form,
            'nav_bar': 'login'
        }
        return render(request, 'mainapp/login.html', context=context)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.add_message(request, messages.INFO, 'Error')
            return redirect('/login/')
