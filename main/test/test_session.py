'''
unit tests for session model
'''
from decimal import Decimal

import logging

from unittest import main
from django.test import TestCase

from main.consumers.staff_session_consumer import take_submit_bid_offer

import main

class TestSession(TestCase):
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

    def test_get_current_session_period(self):
        '''
        test get current session period
        '''
        logger = logging.getLogger(__name__)

        session = main.models.Session.objects.first()
        session.start_experiment()

        #logger.info(f'test_get_current_session_period: {session}')

        session_period = session.get_current_session_period()

        self.assertEqual(1, session_period.period_number)

        session.current_period = 2
        session.save()

        session_period = session.get_current_session_period()

        self.assertEqual(2, session_period.period_number)
    
    def test_session_period(self):
        '''
        test session period bid order
        '''
        logger = logging.getLogger(__name__)

        session = main.models.Session.objects.first()
        session.start_experiment()

        session_period = session.get_current_session_period()

        logger.info(f' session id: {session.id}')

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"b1", "bid_offer_amount":"2.5"})
        self.assertEqual("success", result["status"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"b1", "bid_offer_amount":"3.7"})
        self.assertEqual("success", result["status"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"b1", "bid_offer_amount":"4.1"})
        self.assertEqual("success", result["status"])

        self.assertEqual(session_period.get_bid_list_json(), [{"amount":Decimal('2.5'), "session_period_trade__trade_number":1},
                                                              {"amount":Decimal('3.7'), "session_period_trade__trade_number":1},
                                                              {"amount":Decimal('4.1'), "session_period_trade__trade_number":1}])

        self.assertEqual(session_period.get_current_best_bid().amount, Decimal('4.1'))

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"s1", "bid_offer_amount":"10.5"})
        self.assertEqual("success", result["status"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"s1", "bid_offer_amount":"8"})
        self.assertEqual("success", result["status"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"s1", "bid_offer_amount":"7.23"})
        self.assertEqual("success", result["status"])

        self.assertEqual(session_period.get_offer_list_json(), [{"amount":Decimal('10.5'), "session_period_trade__trade_number":1},
                                                                {"amount":Decimal('8'), "session_period_trade__trade_number":1},
                                                                {"amount":Decimal('7.23'), "session_period_trade__trade_number":1}])

        self.assertEqual(session_period.get_current_best_offer().amount, Decimal('7.23'))

        self.assertEqual(session_period.get_current_trade().trade_number,  1)

        # make trade
        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"s1", "bid_offer_amount":"4.1"})
        self.assertEqual("success", result["status"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"s1", "bid_offer_amount":"6"})
        self.assertEqual("success", result["status"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"b1", "bid_offer_amount":"4"})
        self.assertEqual("success", result["status"])

        self.assertEqual(session_period.get_bid_list_json(), [{"amount":Decimal('2.5'), "session_period_trade__trade_number":1},
                                                              {"amount":Decimal('3.7'), "session_period_trade__trade_number":1},
                                                              {"amount":Decimal('4.1'), "session_period_trade__trade_number":1},
                                                              {"amount":Decimal('4'), "session_period_trade__trade_number":2}])

        self.assertEqual(session_period.get_offer_list_json(), [{"amount":Decimal('10.5'), "session_period_trade__trade_number":1},
                                                                {"amount":Decimal('8'), "session_period_trade__trade_number":1},
                                                                {"amount":Decimal('7.23'), "session_period_trade__trade_number":1},
                                                                {"amount":Decimal('4.1'), "session_period_trade__trade_number":1},
                                                                {"amount":Decimal('6'), "session_period_trade__trade_number":2}])

        session_period = session.get_current_session_period()

        self.assertEqual(session_period.get_current_trade().trade_number,  2)
        self.assertEqual(session_period.get_current_best_bid().amount, Decimal('4'))
        self.assertEqual(session_period.get_current_best_offer().amount, Decimal('6'))
        self.assertEqual(session_period.get_total_gains_from_trade(),  Decimal('9'))

        # check trade list
        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"b2", "bid_offer_amount":"5"})
        self.assertEqual("success", result["status"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"s3", "bid_offer_amount":"5"})
        self.assertEqual("success", result["status"])

        self.assertEqual(session_period.get_total_gains_from_trade(),  Decimal('15'))
        self.assertEqual(session_period.get_period_efficiency(),  '0.60')

        self.assertEqual(len(session_period.get_trade_list_json()), 2)
        self.assertEqual(session_period.get_trade_list_json()[0]['trade_price'], Decimal('4.10'))
        self.assertEqual(session_period.get_trade_list_json()[0]['buyer__session_subject__id_number'], 1)
        self.assertEqual(session_period.get_trade_list_json()[0]['seller__session_subject__id_number'], 1)
        self.assertEqual(session_period.get_trade_list_json()[1]['trade_price'], Decimal('5.00'))
        self.assertEqual(session_period.get_trade_list_json()[1]['buyer__session_subject__id_number'], 2)
        self.assertEqual(session_period.get_trade_list_json()[1]['seller__session_subject__id_number'], 3)

        #check player profit
        b1 = session.session_subjects.get(subject_type=main.globals.SubjectType.BUYER , id_number=1)
        b2 = session.session_subjects.get(subject_type=main.globals.SubjectType.BUYER , id_number=2)
        s1 = session.session_subjects.get(subject_type=main.globals.SubjectType.SELLER , id_number=1)
        s3 = session.session_subjects.get(subject_type=main.globals.SubjectType.SELLER , id_number=3)

        
        self.assertEqual(b1.get_total_profit(),  '5.90')
        self.assertEqual(b2.get_total_profit(),  '4.00')
        self.assertEqual(s1.get_total_profit(),  '3.10')
        self.assertEqual(s3.get_total_profit(),  '2.00')

