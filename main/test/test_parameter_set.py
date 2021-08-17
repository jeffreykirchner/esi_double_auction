'''
unit tests for parameter set model
'''
from decimal import Decimal

import logging
from main.models import parameter_set

from unittest import main
from django.test import TestCase
from django.contrib.auth.models import User
from django.db import transaction

from main.consumers.staff_session_consumer import take_submit_bid_offer

import main

class TestParameterSet(TestCase):
    fixtures = ['auth_user.json', 'main.json']

    user = None
    new_session = None
    start_session = None

    def setUp(self):
        logger = logging.getLogger(__name__)

        # self.user = User.objects.create_user(username='adamsmith', \
        #                                      email='adamsmith@chapman.edu', \
        #                                      password='go panthers')

        # self.user.id=1
        # self.user.save()

        # logger.info(f'create user {self.user}')
        self.user = User.objects.create_user(username='john',
                                 email='jlennon@beatles.com',
                                 password='glass onion')
        
        self.start_session = main.models.Session.objects.first()
        self.new_session = main.consumers.create_new_session(self.user)

    def test_from_dict_fail(self):
        '''
        test create from dict
        '''
        logger = logging.getLogger(__name__)

        session = main.models.Session.objects.get(id=self.start_session.id)
        session.start_experiment()

        #test bad input

        result = session.parameter_set.from_dict({})
        self.assertEqual("fail", result["status"])
        self.assertIn("Failed to load parameter set", result["message"])
    
    def test_from_dict(self):
        '''
        test create from dict
        '''
        logger = logging.getLogger(__name__)

        session = main.models.Session.objects.get(id=self.start_session.id)
        session.start_experiment()

        #test import from another session
        session = main.models.Session.objects.get(id=self.start_session.id)
        self.assertEqual(2, session.parameter_set.number_of_buyers)
        self.assertEqual(1, self.new_session.parameter_set.number_of_buyers)


        result = main.consumers.take_import_parameters({'sessionID': session.id,
                                                        'formData': [{'name': 'session', 'value':str(self.new_session.id)}]})
        self.assertEqual("success", result["status"])

        session = main.models.Session.objects.get(id=self.start_session.id)
        self.assertEqual(1, session.parameter_set.number_of_buyers)

    def test_update_value(self):
        '''
        test updating a value
        '''
        session = main.models.Session.objects.get(id=self.start_session.id)

        value_cost_id = main.models.ParameterSetPeriodSubjectValuecost \
                                   .objects.filter(parameter_set_period_subject__parameter_set_period__parameter_set=
                                                    session.parameter_set).first().id

        #change to 10
        result = main.consumers.take_update_valuecost({'sessionID': session.id,
                                                       'id': value_cost_id,
                                                       'formData': [{'name': 'value_cost', 'value': '10'}, {'name': 'enabled', 'value': 'True'}]})

        self.assertEqual("success", result["value"])
        self.assertEqual(Decimal('10'),  main.models.ParameterSetPeriodSubjectValuecost.objects.get(id=value_cost_id).value_cost)

        #enter invalid amount
        result = main.consumers.take_update_valuecost({'sessionID': session.id,
                                                       'id': value_cost_id,
                                                       'formData': [{'name': 'value_cost', 'value': '-1'}, {'name': 'enabled', 'value': 'True'}]})

        self.assertEqual("fail", result["value"])
        self.assertEqual(Decimal('10'),  main.models.ParameterSetPeriodSubjectValuecost.objects.get(id=value_cost_id).value_cost)

        result = main.consumers.take_update_valuecost({'sessionID': session.id,
                                                       'id': value_cost_id,
                                                       'formData': [{'name': 'value_cost', 'value': 'a'}, {'name': 'enabled', 'value': 'True'}]})

        self.assertEqual("fail", result["value"])
        self.assertEqual(Decimal('10'),  main.models.ParameterSetPeriodSubjectValuecost.objects.get(id=value_cost_id).value_cost)
        
        result = main.consumers.take_update_valuecost({'sessionID': session.id,
                                                       'id': value_cost_id,
                                                       'formData': [{'name': 'value_cost', 'value': '5'}, {'name': 'enabled', 'value': 'a'}]})

        self.assertEqual("fail", result["value"])
        self.assertEqual(Decimal('10'),  main.models.ParameterSetPeriodSubjectValuecost.objects.get(id=value_cost_id).value_cost)
        

    def test_add_shift_delete_buyer(self):  
        '''
        test adding, rotating then deleting a buyer
        '''  

        session = main.models.Session.objects.get(id=self.start_session.id)
        
        self.assertEqual(2, session.parameter_set.number_of_buyers)
    
   

