'''
staff view
'''
import logging

import channels.layers
from asgiref.sync import async_to_sync

from django.views.generic import View
from django.shortcuts import render

from main.models import Parameters

class StaffHomeView(View):
    '''
    class based staff view
    '''
    template_name = "staff_home.html"
    websocket_path = "staff-home"
    
    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''

        #logger = logging.getLogger(__name__) 

        parameters = Parameters.objects.first()

        return render(request, self.template_name, {"parameters" : parameters,
                                                    "page_key" : self.websocket_path,
                                                    "websocket_path" : self.websocket_path})