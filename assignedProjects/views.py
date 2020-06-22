"""
 Views for authentication app.
"""

# python import

# django imports
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from jira import JIRA


class LoginJira(TemplateView):
    """
    Views used  for User Registration Success page
    """
    template_name = 'index.html'

    def get(self, request, **kwargs):
        """
        Method to load login page
        :param kwargs: keyword argument
        :param request: request argument dict type
        :return:Sign up success page
        """
        return render(request, self.template_name, {
        })

    def post(self, request, **kwargs):
        """
         Method used for resend email for verification link
        :param request: argument dict type
        :param kwargs: argument dict type
        :return: redirect to self page
        """
        self.template_name = 'jira_project.html'
        data = request.POST

        jira_options = {'server': 'https://jira.kiwitech.com/'}
        jira = JIRA(options=jira_options, basic_auth=(data['username'], data['password']))
        projects = jira.projects()

        return render(request, self.template_name, {
            'user': request.user,
            'projects': projects
        })


