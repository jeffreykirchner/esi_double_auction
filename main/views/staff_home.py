'''
staff view
'''
import logging

import channels.layers
from asgiref.sync import async_to_sync

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render

class StaffHomeView(TemplateView):
    '''
    class based staff view
    '''
    template_name = "staff_home.html"
    
    def get(self, request):
        '''
        handle get requests
        '''

        logger = logging.getLogger(__name__) 

        return render(request, self.template_name, {"id":""})