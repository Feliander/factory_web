from django.http import HttpResponse
from django.shortcuts import redirect


def redirect_mainapp(request):
    return redirect('home_page_url', permanent=True)
