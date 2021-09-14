'''
staff session paddles view
'''
from django.views import View
from django.shortcuts import render
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import CharField,F, Value

from main.models import Parameters
from main.models import Session
from main.models import HelpDocs

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
        
        try:
            help_text = HelpDocs.objects.annotate(rp=Value(request.path, output_field=CharField()))\
                                       .filter(rp__icontains=F('path')).first().text
        except Exception  as e:   
            help_text = "No help doc was found."

        return render(request=request,
                      template_name=self.template_name,
                      context={"parameters" : parameters,
                               "id" : session.id,
                               "buyer_or_seller" : buyer_or_seller,
                               "buyer_or_seller_count" : buyer_or_seller_count,
                               "rows" : rows,
                               "help_text":help_text,
                               "session" : session})
    
