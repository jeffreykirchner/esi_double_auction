'''
unit tests for bid and offer input
'''
import logging

from unittest import main
from django.test import TestCase

from main.consumers.staff_session_consumer import take_submit_bid_offer

import main

class TestBidOfferInput(TestCase):
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

    def test_bid_offer_input(self):
        '''
        test entering bids and offers
        '''
        logger = logging.getLogger(__name__)

        session = main.models.Session.objects.first()
        session.start_experiment()

        #logger.info(f'test_get_current_session_period: {session}')

        session_period = session.get_current_session_period()

        self.assertEqual(1, session_period.period_number)

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"b1", "bid_offer_amount":"2.5"})
        self.assertEqual("success", result["status"])

        #check valid identifer
        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"", "bid_offer_amount":""})
        self.assertEqual("Error: Invalid ID, missing s or b.", result["message"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"s", "bid_offer_amount":""})
        self.assertEqual("Error: Invalid ID, incorrect number.", result["message"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"sa", "bid_offer_amount":""})
        self.assertEqual("Error: Invalid ID, incorrect number.", result["message"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"s6", "bid_offer_amount":"5"})
        self.assertEqual("Error: Seller 6 does not exist.", result["message"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"b6", "bid_offer_amount":"5"})
        self.assertEqual("Error: Buyer 6 does not exist.", result["message"])

        # check valid amount
        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"b1", "bid_offer_amount":"-1"})
        self.assertEqual("Error: 0 < Amount < 100 .", result["message"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"b1", "bid_offer_amount":"100"})
        self.assertEqual("Error: 0 < Amount < 100 .", result["message"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"b1", "bid_offer_amount":"a"})
        self.assertEqual("Error: Invalid amount, not a decimal.", result["message"])

    def test_excess_trades(self):
        '''
        test entering more bids and offers than allowed
        '''
        logger = logging.getLogger(__name__)

        session = main.models.Session.objects.first()
        session.start_experiment()

        session_period = session.get_current_session_period()

        #check that buyer 2 cannot exceed their total units
        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"b2", "bid_offer_amount":"5"})
        self.assertEqual("success", result["status"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"s1", "bid_offer_amount":"5"})
        self.assertEqual("success", result["status"])

        session_period = session.get_current_session_period()
        self.assertEqual(session_period.get_current_trade().trade_number,  2)

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"b2", "bid_offer_amount":"5"})
        self.assertEqual("success", result["status"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"s1", "bid_offer_amount":"5"})
        self.assertEqual("success", result["status"])

        session_period = session.get_current_session_period()
        self.assertEqual(session_period.get_current_trade().trade_number,  3)

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"b2", "bid_offer_amount":"5"})
        self.assertEqual("success", result["status"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"s1", "bid_offer_amount":"5"})
        self.assertEqual("success", result["status"])

        session_period = session.get_current_session_period()
        self.assertEqual(session_period.get_current_trade().trade_number,  4)

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"b2", "bid_offer_amount":"5"})
        self.assertEqual("fail", result["status"])
        self.assertEqual("Error: Buyer 2 has no units available.", result["message"])

        #check that seller 1 cannot exceed their total units
        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"b1", "bid_offer_amount":"5"})
        self.assertEqual("success", result["status"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"s1", "bid_offer_amount":"5"})
        self.assertEqual("success", result["status"])

        session_period = session.get_current_session_period()
        self.assertEqual(session_period.get_current_trade().trade_number,  5)

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"s1", "bid_offer_amount":"5"})
        self.assertEqual("fail", result["status"])
        self.assertEqual("Error: Seller 1 has no units available.", result["message"])

        session_period = session.get_current_session_period()
        self.assertEqual(session_period.get_current_trade().trade_number,  5)


    def test_price_cap(self):
        '''
        test bids and offers cannot exceed a price cap if enabled
        '''

        logger = logging.getLogger(__name__)

        session = main.models.Session.objects.first()
        session.start_experiment()

        session_period = session.get_current_session_period()
        parameter_set_period = session_period.get_period_parameter_set()

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"b2", "bid_offer_amount":"6"})
        self.assertEqual("success", result["status"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"s1", "bid_offer_amount":"10"})
        self.assertEqual("success", result["status"])

        parameter_set_period.price_cap = 5
        parameter_set_period.price_cap_enabled = True
        parameter_set_period.save()

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"b2", "bid_offer_amount":"7"})
        self.assertEqual("fail", result["status"])
        self.assertEqual("Error: Amount exceeds price cap.", result["message"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"s1", "bid_offer_amount":"9"})
        self.assertEqual("fail", result["status"])
        self.assertEqual("Error: Amount exceeds price cap.", result["message"])
    
    def test_trade(self):
        '''
        test that trade happens at correct price
        '''

        logger = logging.getLogger(__name__)

        session = main.models.Session.objects.first()
        session.start_experiment()

        session_period = session.get_current_session_period()

        #check that offer gets the higher bid price
        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"b2", "bid_offer_amount":"7"})
        self.assertEqual("success", result["status"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"s1", "bid_offer_amount":"6"})
        self.assertEqual("success", result["status"])

        session_period = session.get_current_session_period()
        session_period_trade = session_period.session_period_trades_a.get(trade_number=1)

        self.assertEqual(7, session_period_trade.trade_price)

        #check that bid gets lower offer price
        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"s2", "bid_offer_amount":"6"})
        self.assertEqual("success", result["status"])

        result = take_submit_bid_offer({"sessionID":1, "bid_offer_id":"b1", "bid_offer_amount":"7"})
        self.assertEqual("success", result["status"])

        session_period = session.get_current_session_period()
        session_period_trade = session_period.session_period_trades_a.get(trade_number=2)

        self.assertEqual(6, session_period_trade.trade_price)

        

        
    
   

