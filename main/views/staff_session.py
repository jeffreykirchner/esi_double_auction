'''
staff view
'''
import logging

from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.detail import SingleObjectMixin

from main.models import Parameters
from main.models import Session

from main.forms import SessionForm


class StaffSessionView(SingleObjectMixin, View):
    '''
    class based staff view
    '''
    template_name = "staff_session.html"
    websocket_path = "staff-session"
    model = Session

   
    
    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''

        parameters = Parameters.objects.first()
        session = self.get_object()

        return render(request=request,
                      template_name=self.template_name,
                      context={"parameters" : parameters,
                               "session_form" : SessionForm(),
                               "websocket_path" : self.websocket_path,
                               "page_key" : f'{self.websocket_path}-{session.id}',
                               "session" : session})