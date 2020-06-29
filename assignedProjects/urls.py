"""
Registered assigned projects url.py ..
"""
from django.urls import path
from django.conf.urls.static import static

from kiwiProject import settings
from . import views
# from assignedProjects.my_model import Makedir, Thing
from assignedProjects.congnito import Congneto

from assignedProjects.views import (LoginJira, JiraDashboard, LogoutView)

urlpatterns = [
    path('', LoginJira.as_view(), name="jira_login"),
    # path('mkmodel', Makedir.as_view(), name="mkmodel"),
    # path('book', Thing, name="book"),
    path('cong', Congneto.as_view(), name="cong"),
    path('dashboard', JiraDashboard.as_view(), name="dashboard"),
    path('logout', LogoutView.as_view(), name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
