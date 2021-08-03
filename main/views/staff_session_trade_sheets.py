'''
staff view
'''
import logging
import json

from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from main.models import Parameters, parameter_set
from main.models import Session

from main.forms import SessionForm
from main.forms import ValuecostForm
from main.forms import PeriodForm
from main.forms import ImportParametersForm
from main.forms import SubmitBidOfferStaffForm

class StaffSessionTradeSheetsView(SingleObjectMixin, View):
    '''
    class based staff session payout view
    '''
    template_name = "staff/staff_session_trade_sheets.html"
    websocket_path = "staff-session-trade-sheets"
    model = Session
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''

        parameters = Parameters.objects.first()
        session = self.get_object()
        
        buyer_list = session.parameter_set.get_buyer_list_json()

        return render(request=request,
                      template_name=self.template_name,
                      context={"parameters" : parameters,
                               "id" : session.id,
                               "session" : session,
                               "buyer_list" : buyer_list,
                               "parameter_set" : parameter_set})
    
