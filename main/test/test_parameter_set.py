'''
unit tests for parameter set model
'''
from decimal import Decimal

import logging
from main.models import parameter_set, parameter_set_period_subject

from unittest import main, result
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
        
        parameter_set_period_subject = main.models.ParameterSetPeriodSubject.objects.get(parameter_set_period__parameter_set=session.parameter_set,
                                                                                         parameter_set_period__period_number=1,
                                                                                         id_number=1,
                                                                                         subject_type=main.globals.SubjectType.BUYER) 
        
        self.assertEqual(10, parameter_set_period_subject.get_value_cost_list()[0].value_cost)

        #add buyer
        result = main.consumers.take_update_subject_count({'sessionID': 1, 'current_visible_period': 1, 'type': 'BUYER', 'adjustment': 1})
        self.assertEqual("success", result)

        #shift values
        result = main.consumers.take_shift_value_or_cost({'sessionID': 1, 'currentPeriod': 1, 'valueOrCost': 'value', 'direction': 'up'})
        self.assertEqual("success", result)

        parameter_set_period_subject = main.models.ParameterSetPeriodSubject.objects.get(parameter_set_period__parameter_set=session.parameter_set,
                                                                                         parameter_set_period__period_number=1,
                                                                                         id_number=1,
                                                                                         subject_type=main.globals.SubjectType.BUYER) 
        
        self.assertEqual(9, parameter_set_period_subject.get_value_cost_list()[0].value_cost)

        result = main.consumers.take_shift_value_or_cost({'sessionID': 1, 'currentPeriod': 1, 'valueOrCost': 'value', 'direction': 'up'})
        self.assertEqual("success", result)

        parameter_set_period_subject = main.models.ParameterSetPeriodSubject.objects.get(parameter_set_period__parameter_set=session.parameter_set,
                                                                                         parameter_set_period__period_number=1,
                                                                                         id_number=1,
                                                                                         subject_type=main.globals.SubjectType.BUYER) 
        
        self.assertEqual(0, parameter_set_period_subject.get_value_cost_list()[0].value_cost)

        result = main.consumers.take_shift_value_or_cost({'sessionID': 1, 'currentPeriod': 1, 'valueOrCost': 'value', 'direction': 'down'})
        self.assertEqual("success", result)

        parameter_set_period_subject = main.models.ParameterSetPeriodSubject.objects.get(parameter_set_period__parameter_set=session.parameter_set,
                                                                                         parameter_set_period__period_number=1,
                                                                                         id_number=1,
                                                                                         subject_type=main.globals.SubjectType.BUYER) 
        
        self.assertEqual(9, parameter_set_period_subject.get_value_cost_list()[0].value_cost)

        #delete buyer
        session = main.models.Session.objects.get(id=self.start_session.id)
        self.assertEqual(3, session.parameter_set.number_of_buyers)

        result = main.consumers.take_update_subject_count({'sessionID': 1, 'current_visible_period': 1, 'type': 'BUYER', 'adjustment': -1})
        self.assertEqual("success", result)

        session = main.models.Session.objects.get(id=self.start_session.id)
        self.assertEqual(2, session.parameter_set.number_of_buyers)

        parameter_set_period_subject = main.models.ParameterSetPeriodSubject.objects.get(parameter_set_period__parameter_set=session.parameter_set,
                                                                                         parameter_set_period__period_number=1,
                                                                                         id_number=1,
                                                                                         subject_type=main.globals.SubjectType.BUYER) 
        
        self.assertEqual(9, parameter_set_period_subject.get_value_cost_list()[0].value_cost)

        #add amount to all
        result = main.consumers.take_add_to_all_values_or_costs({'sessionID': 1, 'currentPeriod': 1, 'valueOrCost': 'value', 'amount': '0.01'})
        self.assertEqual("success", result)

        parameter_set_period_subject = main.models.ParameterSetPeriodSubject.objects.get(parameter_set_period__parameter_set=session.parameter_set,
                                                                                         parameter_set_period__period_number=1,
                                                                                         id_number=1,
                                                                                         subject_type=main.globals.SubjectType.BUYER) 
        
        self.assertEqual(Decimal('9.01'), parameter_set_period_subject.get_value_cost_list()[0].value_cost)

    def test_add_shift_delete_seller(self):  
        '''
        test adding, rotating then deleting a seller
        '''  

        session = main.models.Session.objects.get(id=self.start_session.id)
        
        self.assertEqual(3, session.parameter_set.number_of_sellers)
        
        parameter_set_period_subject = main.models.ParameterSetPeriodSubject.objects.get(parameter_set_period__parameter_set=session.parameter_set,
                                                                                         parameter_set_period__period_number=1,
                                                                                         id_number=1,
                                                                                         subject_type=main.globals.SubjectType.SELLER) 
        
        self.assertEqual(1, parameter_set_period_subject.get_value_cost_list()[0].value_cost)

        #add seller
        result = main.consumers.take_update_subject_count({'sessionID': 1, 'current_visible_period': 1, 'type': 'SELLER', 'adjustment': 1})
        self.assertEqual("success", result)

        #shift values
        result = main.consumers.take_shift_value_or_cost({'sessionID': 1, 'currentPeriod': 1, 'valueOrCost': 'cost', 'direction': 'up'})
        self.assertEqual("success", result)

        parameter_set_period_subject = main.models.ParameterSetPeriodSubject.objects.get(parameter_set_period__parameter_set=session.parameter_set,
                                                                                         parameter_set_period__period_number=1,
                                                                                         id_number=1,
                                                                                         subject_type=main.globals.SubjectType.SELLER) 
        
        self.assertEqual(2, parameter_set_period_subject.get_value_cost_list()[0].value_cost)

        result = main.consumers.take_shift_value_or_cost({'sessionID': 1, 'currentPeriod': 1, 'valueOrCost': 'cost', 'direction': 'up'})
        self.assertEqual("success", result)

        parameter_set_period_subject = main.models.ParameterSetPeriodSubject.objects.get(parameter_set_period__parameter_set=session.parameter_set,
                                                                                         parameter_set_period__period_number=1,
                                                                                         id_number=1,
                                                                                         subject_type=main.globals.SubjectType.SELLER) 
        
        self.assertEqual(3, parameter_set_period_subject.get_value_cost_list()[0].value_cost)

        result = main.consumers.take_shift_value_or_cost({'sessionID': 1, 'currentPeriod': 1, 'valueOrCost': 'cost', 'direction': 'down'})
        self.assertEqual("success", result)

        parameter_set_period_subject = main.models.ParameterSetPeriodSubject.objects.get(parameter_set_period__parameter_set=session.parameter_set,
                                                                                         parameter_set_period__period_number=1,
                                                                                         id_number=1,
                                                                                         subject_type=main.globals.SubjectType.SELLER) 
        
        self.assertEqual(2, parameter_set_period_subject.get_value_cost_list()[0].value_cost)

        #delete seller
        session = main.models.Session.objects.get(id=self.start_session.id)
        self.assertEqual(4, session.parameter_set.number_of_sellers)

        result = main.consumers.take_update_subject_count({'sessionID': 1, 'current_visible_period': 1, 'type': 'SELLER', 'adjustment': -1})
        self.assertEqual("success", result)

        session = main.models.Session.objects.get(id=self.start_session.id)
        self.assertEqual(3, session.parameter_set.number_of_sellers)

        parameter_set_period_subject = main.models.ParameterSetPeriodSubject.objects.get(parameter_set_period__parameter_set=session.parameter_set,
                                                                                         parameter_set_period__period_number=1,
                                                                                         id_number=1,
                                                                                         subject_type=main.globals.SubjectType.SELLER) 
        
        self.assertEqual(2, parameter_set_period_subject.get_value_cost_list()[0].value_cost)

        #add amount to all
        result = main.consumers.take_add_to_all_values_or_costs({'sessionID': 1, 'currentPeriod': 1, 'valueOrCost': 'cost', 'amount': '0.01'})
        self.assertEqual("success", result)

        parameter_set_period_subject = main.models.ParameterSetPeriodSubject.objects.get(parameter_set_period__parameter_set=session.parameter_set,
                                                                                         parameter_set_period__period_number=1,
                                                                                         id_number=1,
                                                                                         subject_type=main.globals.SubjectType.SELLER) 
        
        self.assertEqual(Decimal('2.01'), parameter_set_period_subject.get_value_cost_list()[0].value_cost)

    def test_add_period_copy_values_and_costs(self):
        '''
        add a period then copy values and costs from previous period
        '''
        session = main.models.Session.objects.get(id=self.start_session.id)
        self.assertEqual(2, session.parameter_set.parameter_set_periods.count())

        #add period
        result = main.consumers.take_update_period_count({'sessionID': 1, 'adjustment': 1})
        self.assertEqual("success", result)

        session = main.models.Session.objects.get(id=self.start_session.id)
        self.assertEqual(3, session.parameter_set.parameter_set_periods.count())

        #copy values
        session = main.models.Session.objects.get(id=self.start_session.id)
        parameter_set_period_subject = main.models.ParameterSetPeriodSubject.objects.get(parameter_set_period__parameter_set=session.parameter_set,
                                                                                         parameter_set_period__period_number=3,
                                                                                         id_number=1,
                                                                                         subject_type=main.globals.SubjectType.BUYER) 
        
        self.assertEqual(0, parameter_set_period_subject.get_value_cost_list()[0].value_cost)

        result = main.consumers.take_copy_value_or_cost({'sessionID': 1, 'currentPeriod': 3, 'valueOrCost': 'value'})
        self.assertEqual("success", result)

        session = main.models.Session.objects.get(id=self.start_session.id)
        parameter_set_period_subject = main.models.ParameterSetPeriodSubject.objects.get(parameter_set_period__parameter_set=session.parameter_set,
                                                                                         parameter_set_period__period_number=3,
                                                                                         id_number=1,
                                                                                         subject_type=main.globals.SubjectType.BUYER) 
        
        self.assertEqual(Decimal('12.00'), parameter_set_period_subject.get_value_cost_list()[0].value_cost)

        #copy costs
        session = main.models.Session.objects.get(id=self.start_session.id)
        parameter_set_period_subject = main.models.ParameterSetPeriodSubject.objects.get(parameter_set_period__parameter_set=session.parameter_set,
                                                                                         parameter_set_period__period_number=3,
                                                                                         id_number=1,
                                                                                         subject_type=main.globals.SubjectType.SELLER) 
        
        self.assertEqual(0, parameter_set_period_subject.get_value_cost_list()[0].value_cost)

        result = main.consumers.take_copy_value_or_cost({'sessionID': 1, 'currentPeriod': 3, 'valueOrCost': 'cost'})
        self.assertEqual("success", result)

        session = main.models.Session.objects.get(id=self.start_session.id)
        parameter_set_period_subject = main.models.ParameterSetPeriodSubject.objects.get(parameter_set_period__parameter_set=session.parameter_set,
                                                                                         parameter_set_period__period_number=3,
                                                                                         id_number=1,
                                                                                         subject_type=main.globals.SubjectType.SELLER) 
        
        self.assertEqual(Decimal('2.00'), parameter_set_period_subject.get_value_cost_list()[0].value_cost)

    def test_parameter_set_period_parameters(self):
        '''
        test updating period parameters
        '''
        session = main.models.Session.objects.get(id=self.start_session.id)
        parameter_set_period = main.models.ParameterSetPeriod.objects.get(parameter_set=session.parameter_set,
                                                                          period_number=1)

        result = main.consumers.take_update_period({'sessionID': session.id,
                                                    'periodID': parameter_set_period.id,
                                                    'formData': [{'name': 'price_cap', 'value': '0.00'},
                                                                 {'name': 'price_cap_enabled', 'value': 'False'},
                                                                 {'name': 'y_scale_max', 'value': '1'},
                                                                 {'name': 'x_scale_max', 'value': '11'}]})
        
        self.assertEqual("success", result["value"])

        # invalid price cap
        result = main.consumers.take_update_period({'sessionID': session.id,
                                                    'periodID': parameter_set_period.id,
                                                    'formData': [{'name': 'price_cap', 'value': '-1'},
                                                                 {'name': 'price_cap_enabled', 'value': 'False'},
                                                                 {'name': 'y_scale_max', 'value': '1'},
                                                                 {'name': 'x_scale_max', 'value': '11'}]})
        
        self.assertEqual("fail", result["value"])

        # invalid price cap
        result = main.consumers.take_update_period({'sessionID': session.id,
                                                    'periodID': parameter_set_period.id,
                                                    'formData': [{'name': 'price_cap', 'value': '0.00'},
                                                                 {'name': 'price_cap_enabled', 'value': 'a'},
                                                                 {'name': 'y_scale_max', 'value': '1'},
                                                                 {'name': 'x_scale_max', 'value': '11'}]})
        
        self.assertEqual("fail", result["value"])

        #invalid y scale max
        result = main.consumers.take_update_period({'sessionID': session.id,
                                                    'periodID': parameter_set_period.id,
                                                    'formData': [{'name': 'price_cap', 'value': '0.00'},
                                                                 {'name': 'price_cap_enabled', 'value': 'False'},
                                                                 {'name': 'y_scale_max', 'value': '0'},
                                                                 {'name': 'x_scale_max', 'value': '11'}]})
        
        self.assertEqual("fail", result["value"])

        # invalid x scale max
        result = main.consumers.take_update_period({'sessionID': session.id,
                                                    'periodID': parameter_set_period.id,
                                                    'formData': [{'name': 'price_cap', 'value': '0.00'},
                                                                 {'name': 'price_cap_enabled', 'value': 'False'},
                                                                 {'name': 'y_scale_max', 'value': '1'},
                                                                 {'name': 'x_scale_max', 'value': '0'}]})
        
        self.assertEqual("fail", result["value"])








        
   

