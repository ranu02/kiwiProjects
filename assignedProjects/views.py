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
from jira.client import GreenHopper
from jira.resources import GreenHopperResource



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
            data = []
            for p_data in projects:
                if p_data.id:
                    val = {'jira': p_data, 'details': jira.project(p_data.id)}
                    data.append(val)
            # first_project = jira.project(projects[0].id)
            # onboard = jira.boards(maxResults=1, type='scrum')
            #
            # sprint = jira.sprints(jira.boards()[0].id)
            #
            # jira.sprint_info(jira.boards()[0].id, sprint[0].id)
            # oh_crap = jira.search_issues('assignee = currentUser()',
            #                              maxResults=50)

            # issues_in_project = jira.search_issues(
            #     'project=12118 AND SPRINT not in closedSprints() AND sprint in futureSprints()')
            return render(request, self.template_name, {
                'user': request.user,
                'projects': data,
                'request': request
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
