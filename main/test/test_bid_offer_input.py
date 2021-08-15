'''
unit tests for session model
'''
import decimal
from asgiref.sync import async_to_sync
from decimal import Decimal

import logging
import asyncio

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
        

        
    
   

