'''
unit tests for parameter set model
'''
import decimal
from main.models import parameter_set_period
from asgiref.sync import async_to_sync
from decimal import Decimal

import logging

from unittest import main
from django.test import TestCase

from main.consumers.staff_session_consumer import take_submit_bid_offer

import main

class TestParameterSet(TestCase):
    fixtures = ['auth_user.json', 'main.json']

    user = None

    def setUp(self):
        logger = logging.getLogger(__name__)

        # self.user = User.objects.create_user(username='adamsmith', \
        #                                      email='adamsmith@chapman.edu', \
        #                                      password='go panthers')

        # self.user.id=1
        # self.user.save()

        # logger.info(f'create user {self.user}')

    def test_from_dict(self):
        '''
        test create from dict
        '''
        logger = logging.getLogger(__name__)

        

        

        
    
   

