import math

from django.shortcuts import render
from django import views

from .utils import (
    lagrang_get_table,
    newtone_get_table,
)

class Lab31(views.View):
    def get(self, request):
        return render(request, 'lab31/lab31.html', {
            # Debugging
            # **lagrang_get_table(0.1, 0.5, 0.9, 1.3, 'a'),
            # **newtone_get_table(0, 1, 2, 3, 'a'),

            **lagrang_get_table(0, math.pi / 6,
                                2 * math.pi / 6, 3 * math.pi / 6, 'a'),
            **lagrang_get_table(0, math.pi / 6,
                                5 * math.pi / 12, math.pi / 2, 'b'),
            **newtone_get_table(0, math.pi / 6,
                                2 * math.pi / 6, 3 * math.pi / 6, 'a'),
            **newtone_get_table(0, math.pi / 6,
                                5 * math.pi / 12, math.pi / 2, 'b'),
        })