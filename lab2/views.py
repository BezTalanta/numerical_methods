import math

from django.shortcuts import render
from django.contrib.messages import error
from django import views

from .utils import (
    simple_newtone_method,
    simple_iterations,

    hard_newtone_method,
    hard_iteration_method,
)


class Lab21(views.View):
    def get(self, request):
        return render(request, 'lab21/lab21.html')

    def post(self, request):
        # a, b = 0, 0.6
        try:
            eps = request.POST['precision']
        except Exception as e:
            error('Your precision is bad, try again')
            print(e)
            return render(request, 'lab21/lab21.html')

        return render(request, 'lab21/result.html', {
            **simple_newtone_method(eps),
            **simple_iterations(eps),
        })


class Lab22(views.View):
    def get(self, request):
        return render(request, 'lab22/lab22.html')

    def post(self, request):
        try:
            eps = request.POST['precision']
        except Exception as e:
            error('Your precision is bad, try again')
            print(e)
            return render(request, 'lab22/lab22.html')

        return render(request, 'lab22/result.html', {
            **hard_newtone_method(eps),
            **hard_iteration_method(eps),
        })
