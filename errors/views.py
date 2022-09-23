from django.shortcuts import render
from django.http import HttpResponse


def server_error(request, template_name='err_pages/500.html'):
    return render(request, template_name)


def not_found(request):
    return render(request, 'err_pages/404.html')


def e400(request):
    return render(request, 'err_pages/400.html')