from django.urls import path

from .views import (
    Lab31,
)

urlpatterns = [
    path('1', Lab31.as_view(), name='31'),
    path('2', Lab31.as_view(), name='32'),
    path('3', Lab31.as_view(), name='33'),
    path('4', Lab31.as_view(), name='34'),
    path('5', Lab31.as_view(), name='35'),
]