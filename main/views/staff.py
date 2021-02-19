'''
staff view
'''
import logging

import channels.layers
from asgiref.sync import async_to_sync

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render

class StaffView(TemplateView):
    '''
    class based staff view
    '''
    template_name = "staff_home.html"

    def get(self, request):
        '''
        handle get requests
        '''

        logger = logging.getLogger(__name__) 

        # channel_layer = channels.layers.get_channel_layer()
        # async_to_sync(channel_layer.send)('test_channel', {'type': 'hello'})

        # v = async_to_sync(channel_layer.receive)('test_channel')

        # logger.info(v)

        return render(request, self.template_name, {"id":""})
    

    def post(self, request):
        '''
        handle post requests
        '''

        return JsonResponse({"response" : "fail"}, safe=False)