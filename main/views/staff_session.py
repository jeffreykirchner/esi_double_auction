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
    model = Session
    
    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''
        
        parameters = Parameters.objects.first()

        return render(request, self.template_name, {"parameters" : parameters,
                                                    "session_form" : SessionForm(),
                                                    "websocket_path" : "staff-session",
                                                    "session" : self.get_object()})