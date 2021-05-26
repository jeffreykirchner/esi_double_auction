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
from main.forms import ValuecostForm
from main.forms import PeriodForm

class StaffSessionView(SingleObjectMixin, View):
    '''
    class based staff view
    '''
    template_name = "staff/staff_session.html"
    websocket_path = "staff-session"
    model = Session
    
    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''

        parameters = Parameters.objects.first()
        session = self.get_object()

        valuecost_form_ids=[]
        for i in ValuecostForm():
            valuecost_form_ids.append(i.html_name)

        period_form_ids=[]
        for i in PeriodForm():
            period_form_ids.append(i.html_name)

        return render(request=request,
                      template_name=self.template_name,
                      context={"parameters" : parameters,
                               "session_form" : SessionForm(),
                               "valuecost_form" : ValuecostForm(),
                               "valuecost_form_ids" : valuecost_form_ids,
                               "period_form" : PeriodForm(),
                               "period_form_ids" : period_form_ids,
                               "websocket_path" : self.websocket_path,
                               "page_key" : f'{self.websocket_path}-{session.id}',
                               "session" : session})