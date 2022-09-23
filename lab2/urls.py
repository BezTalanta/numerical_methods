from django.urls import path

from .views import (
    Lab21,
    Lab22,
)

urlpatterns = [
    path('1', Lab21.as_view(), name='21'),
    path('2', Lab22.as_view(), name='22'),
]
