import math

from django.shortcuts import render, redirect
from django.urls import reverse
from django import views

from .utils import (
    # 1
    lagrang_get_table,
    newtone_get_table,

    # 2
    run_through_32,

    # 3
    run_through_33,
)

class Lab31(views.View):
    def get(self, request):
        return render(request, 'lab31/lab31.html', {
            # Debugging
            # **lagrang_get_table(0.1, 0.5, 0.9, 1.3, 'a'),
            # **newtone_get_table(0, 1, 2, 3, 'a'),
            #

            **lagrang_get_table(0, math.pi / 6,
                                2 * math.pi / 6, 3 * math.pi / 6, 'a'),
            **lagrang_get_table(0, math.pi / 6,
                                5 * math.pi / 12, math.pi / 2, 'b'),
            **newtone_get_table(0, math.pi / 6,
                                2 * math.pi / 6, 3 * math.pi / 6, 'a'),
            **newtone_get_table(0, math.pi / 6,
                                5 * math.pi / 12, math.pi / 2, 'b'),
        })


class Lab32(views.View):
    def get(self, request):
        return render(request, 'lab32/lab32.html', {
            **run_through_32(),
        })

class Lab33(views.View):
    def get(self, request):
        return render(request, 'lab33/lab33.html',{
            **run_through_33(),
        })
