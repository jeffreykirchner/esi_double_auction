'''
staff view
'''
import logging
import uuid

import channels.layers
from asgiref.sync import async_to_sync

from django.views.generic import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import CharField,F, Value

from main.models import Parameters
from main.models import HelpDocs

class StaffHomeView(View):
    '''
    class based staff view
    '''
    template_name = "staff/staff_home.html"
    websocket_path = "staff-home"
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''

        #logger = logging.getLogger(__name__) 

        parameters = Parameters.objects.first()

        try:
            help_text = HelpDocs.objects.annotate(rp=Value(request.path,output_field=CharField()))\
                                       .filter(rp__icontains=F('path')).first().text
        except Exception  as e:   
             help_text = "No help doc was found."

        return render(request, self.template_name, {"channel_key" : uuid.uuid4(),
                                                    "page_key" : "staff-home",
                                                    "help_text":help_text,
                                                    "websocket_path" : self.websocket_path})