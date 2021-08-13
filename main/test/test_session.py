'''
unit tests for session model
'''

import logging

from unittest import main
from django.test import TestCase
from django.contrib.auth.models import User

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
        test auto pay feature
        '''
        logger = logging.getLogger(__name__)

        session = main.models.Session.objects.first()

        logger.info(f'test_get_current_session_period: {session}')

