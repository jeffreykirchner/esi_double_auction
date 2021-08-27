'''
staff record sheet demo
'''
import json

from django.views.generic import View
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import CharField,F, Value

from main.models import Parameters
from main.models import HelpDocs

class StaffDemo(View):
    '''
    class based staff view
    '''
    template_name = "staff/staff_demo.html"
    websocket_path = "staff-demo"
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''

        #logger = logging.getLogger(__name__) 

        parameters = Parameters.objects.first()

        buyer = {"periods":[{"id_number" : 1,
                              "value_list": [{"value_cost" : "10.00", "enabled" : True},
                                             {"value_cost" : "8.00", "enabled" : True},
                                             {"value_cost" : "6.00", "enabled" : True},
                                             {"value_cost" : "4.00", "enabled" : True}]
                            }]
                }
        
        seller = {"periods":[{"id_number" : 1,
                              "cost_list": [{"value_cost" : "5.00", "enabled" : True},
                                             {"value_cost" : "7.00", "enabled" : True},
                                             {"value_cost" : "9.00", "enabled" : True},
                                             {"value_cost" : "11.00", "enabled" : True}]
                            }]
                 }
        
        try:
            help_text = HelpDocs.objects.annotate(rp=Value(request.path,output_field=CharField()))\
                                       .filter(rp__icontains=F('path')).first().text
        except Exception  as e:   
             help_text = "No help doc was found."

        return render(request, self.template_name, {"buyer" : buyer,
                                                    "buyer_json" : json.dumps(buyer, cls=DjangoJSONEncoder),
                                                    "seller" : seller,
                                                    "help_text":help_text,
                                                    "seller_json" : json.dumps(seller, cls=DjangoJSONEncoder),
                                                    "editable" : True})