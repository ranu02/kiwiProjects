# django imports
from django import template
# django imports
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View
from jira import JIRA, JIRAError
import logging

register = template.Library()


@register.simple_tag
def get_project_details(request, id):
    """
    Get Category
    :return: Category Id
    """
    data = None
    username = request.session['username']
    password = request.session['password']
    jira_options = {'server': 'https://jira.kiwitech.com/', 'verify': True}
    try:
        jira = JIRA(options=jira_options, basic_auth=(username, password), max_retries=0)
        data = jira.project(id)
        # save session with state full
    except JIRAError as e:
        logging.error("Failed to connect to JIRA: %s" % e)
    return data