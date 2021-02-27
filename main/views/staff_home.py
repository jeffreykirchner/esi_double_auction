'''
staff view
'''
import logging
import json

import channels.layers
from asgiref.sync import async_to_sync

from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse

from main.models import Parameters

class StaffHomeView(View):
    '''
    class based staff view
    '''
    template_name = "staff_home.html"
    websocket_path = "staff-home"

    def post(self, request, *args, **kwargs):
        '''
        handle post request
        '''
        data = json.loads(request.body.decode('utf-8'))

        logger = logging.getLogger(__name__) 
        logger.info(data)

        return JsonResponse({"response" : "some data"}, safe=False)
    
    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''

        #logger = logging.getLogger(__name__) 

        parameters = Parameters.objects.first()

        return render(request, self.template_name, {"parameters" : parameters,
                                                    "page_key" : self.websocket_path,
                                                    "websocket_path" : self.websocket_path})