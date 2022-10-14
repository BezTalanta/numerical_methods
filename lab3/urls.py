from django.urls import path

from .views import (
    Lab31,
    Lab32,
    Lab33,
    Lab34,
    Lab35,
)

urlpatterns = [
    path('1', Lab31.as_view(), name='31'),
    path('2', Lab32.as_view(), name='32'),
    path('3', Lab33.as_view(), name='33'),
    path('4', Lab34.as_view(), name='34'),
    path('5', Lab35.as_view(), name='35'),
]
