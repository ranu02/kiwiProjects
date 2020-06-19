"""
Registered assigned projects url.py ..
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
]
