from django.urls import path

from .views import(
    Lab11,
    Lab12,
    Lab13,
    Lab14,
    Lab15,
)

urlpatterns = [
    path('1/', Lab11.as_view(), name='11'),
    path('2/', Lab12.as_view(), name='12'),
    path('3/', Lab13.as_view(), name='13'),
    path('4/', Lab14.as_view(), name='14'),
    path('5/', Lab15.as_view(), name='15'),
]

'''
3:
    Диагональ != 0
'''
