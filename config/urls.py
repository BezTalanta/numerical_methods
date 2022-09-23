from django.contrib import admin
from django.urls import path, include

from .start_view import StartView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', StartView.as_view(), name='home'),
    path('lab1/', include('lab1.urls')),
    path('lab2/', include('lab2.urls')),
]

handler500 = 'errors.views.server_error'
hadnler404 = 'errors.views.not_found'
