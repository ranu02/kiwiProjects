"""
 Views for authentication app.
"""

# python import

# django imports
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View
from jira import JIRA, JIRAError
import logging


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
        if request.session.has_key('username') and request.session.has_key('password'):
            return redirect('dashboard')
        return render(request, self.template_name, {
        })

    def post(self, request, **kwargs):
        """
         Method used for resend email for verification link
        :param request: argument dict type
        :param kwargs: argument dict type
        :return: redirect to self page
        """
        data = request.POST
        jira_options = {'server': 'https://jira.kiwitech.com/', 'verify': True}
        try:
            JIRA(options=jira_options, basic_auth=(data['username'], data['password']), max_retries=0)
            # save session with state full
            request.session['username'] = data['username']
            request.session['password'] = data['password']
        except JIRAError as e:
            logging.error("Failed to connect to JIRA: %s" % e)
            return render(request, self.template_name, {
                'wrong_msg': True
            })
        return redirect('dashboard')


class JiraDashboard(TemplateView):
    """
    Views used  for User Registration Success page
    """
    template_name = 'jira_project.html'

    def get(self, request, **kwargs):
        """
        Method to load login page
        :param kwargs: keyword argument
        :param request: request argument dict type
        :return:Sign up success page
        """
        username = None
        password = None
        if request.session.has_key('username') and request.session.has_key('password'):
            username = request.session['username']
            password = request.session['password']
        jira_options = {'server': 'https://jira.kiwitech.com/', 'verify': True}
        try:
            jira = JIRA(options=jira_options, basic_auth=(username, password), max_retries=0)
            projects = jira.projects()
            return render(request, self.template_name, {
                'user': request.user,
                'projects': projects
            })
        except JIRAError as e:
            logging.error("Failed to connect to JIRA: %s" % e)
            return redirect('login')


class LogoutView(View):
    """
    View is used for logout
    """
    @staticmethod
    def get(request):
        """
        Method used to logout user
        :param request: GET request
        :return:redirect to login page
        """
        try:
            del request.session['username']
            del request.session['password']
        except:
            pass
        return redirect('jira_login')
