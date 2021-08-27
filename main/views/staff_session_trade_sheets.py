'''
staff session trade sheets view
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

from main.decorators import user_is_owner

class StaffSessionTradeSheetsView(SingleObjectMixin, View):
    '''
    class based staff session payout view
    '''
    template_name = "staff/staff_session_trade_sheets.html"
    websocket_path = "staff-session-trade-sheets"
    model = Session
    
    @method_decorator(login_required)
    @method_decorator(user_is_owner)
    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''

        parameters = Parameters.objects.first()
        session = self.get_object()
        
        buyer_list = session.parameter_set.get_buyer_list_json()
        seller_list = session.parameter_set.get_seller_list_json()

        try:
            help_text = HelpDocs.objects.annotate(rp=Value(request.path,output_field=CharField()))\
                                       .filter(rp__icontains=F('path')).first().text
        except Exception  as e:   
             help_text = "No help doc was found."

        return render(request=request,
                      template_name=self.template_name,
                      context={"parameters" : parameters,
                               "id" : session.id,
                               "session" : session,
                               "buyer_list" : buyer_list,
                               "seller_list" : seller_list,
                               "help_text":help_text,
                               "editable":False})
    
