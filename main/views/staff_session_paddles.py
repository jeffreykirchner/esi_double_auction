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

class StaffSessionPaddles(SingleObjectMixin, View):
    '''
    class based staff session paddle printouts view
    '''
    template_name = "staff/staff_session_paddles.html"
    websocket_path = "staff-session-paddles"
    model = Session
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''

        parameters = Parameters.objects.first()
        session = self.get_object()

        rows = []

        if kwargs['buyer_or_seller'] == "Buyer":
            buyer_or_seller = "Buyer"
        else:
            buyer_or_seller = "Seller"

        return render(request=request,
                      template_name=self.template_name,
                      context={"parameters" : parameters,
                               "id" : session.id,
                               "buyer_or_seller" : buyer_or_seller,
                               "rows" : rows,
                               "session" : session})
    
