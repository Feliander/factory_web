import time
import datetime
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.template import loader


from .forms import *
from .models import *


def logout_view(request):
    logout(request)
    return redirect('/')


def timer2(value='start'):
    t = 0
    while value == 'start':
        t += 1
        print(t)
        time.sleep(1)


class Main(View):

    def get(self, request):
        if request.is_ajax():
            if Employee.objects.filter(user__exact=request.user.pk).count():
                date_time = request.GET.get('button_text')
                if date_time == 'stop':
                    response = HttpResponse()
                    response.delete_cookie("date_time")
                    return response
                else:
                    if "date_time" in request.COOKIES:
                        return JsonResponse({'seconds': request.COOKIES['date_time']}, status=200)
                    else:
                        if date_time:
                            response = HttpResponse()
                            response.set_cookie("date_time", date_time)
                            return response
        if request.user.is_authenticated:
            context = {
                'nav_bar': 'home'
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
                clicked = 'True'
                bound_form.save()
                return redirect('/')
            return render(request, 'mainapp/main.html')
        else:
            return redirect('/create-employee/')


class CreateAnEmployee(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        if request.user.is_authenticated:
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
        else:
            return redirect('/login/')

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
        form = LoginForm()
        context = {
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


class PersonalArea(View):

    def get(self, request):
        username = request.user
        context = {
            'username': username,
            'nav_bar': 'user'
        }
        return render(request, 'mainapp/personal_area.html', context=context)
