"""
Registered assigned projects url.py ..
"""
from django.urls import path
from django.conf.urls.static import static

from kiwiProject import settings
from . import views
from assignedProjects.views import (LoginJira, JiraDashboard, LogoutView)

urlpatterns = [
    path('', LoginJira.as_view(), name="jira_login"),
    path('dashboard', JiraDashboard.as_view(), name="dashboard"),
    path('logout', LogoutView.as_view(), name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
