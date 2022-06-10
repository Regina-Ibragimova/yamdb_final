from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'users'

router = DefaultRouter()

urlpatterns = [
    path('signup/', views.create_user, name='create_user'),
    path('token/', views.get_token, name='get_token'),
]
