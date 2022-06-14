from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', lambda red: redirect('redoc/')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('redoc/', TemplateView.as_view(template_name='redoc.html'),
         name='redoc'),
]
