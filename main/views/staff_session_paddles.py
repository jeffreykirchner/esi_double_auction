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
        col = []

        if kwargs['buyer_or_seller'] == "Buyer":
            buyer_or_seller = "Buyer"          
            buyer_or_seller_count = session.parameter_set.number_of_buyers
        else:
            buyer_or_seller = "Seller"
            buyer_or_seller_count = session.parameter_set.number_of_sellers

        for i in range(buyer_or_seller_count):

            if buyer_or_seller == "Buyer":
                col.append(f"B{i+1}")
            else:
                col.append(f"S{i+1}")

            if i % 2 == 1 or i == buyer_or_seller_count-1:
                rows.append(col)
                col = []

        return render(request=request,
                      template_name=self.template_name,
                      context={"parameters" : parameters,
                               "id" : session.id,
                               "buyer_or_seller" : buyer_or_seller,
                               "buyer_or_seller_count" : buyer_or_seller_count,
                               "rows" : rows,
                               "session" : session})
    
