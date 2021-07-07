'''
session period trade bid model
'''

#import logging

from django.db import models

from . import SessionPeriodTrade
from . import ParameterSetPeriodSubjectValuecost

class SessionPeriodTradeBid(models.Model):
    '''
    session period trade bid model
    '''
    session_period_trade = models.ForeignKey(SessionPeriodTrade, on_delete=models.CASCADE, related_name="session_period_trade_bids")
    value = models.ForeignKey(ParameterSetPeriodSubjectValuecost, on_delete=models.CASCADE, related_name="session_period_trade_bids_value")
    session_subject_period =  models.ForeignKey('main.SessionSubjectPeriod', on_delete=models.CASCADE, related_name="session_period_trade_bids_b")

    amount = models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Bid Amount')

    timestamp = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = 'Session Period Trade Bid'
        verbose_name_plural = 'Session Period Trade Bids'
        ordering = ['-amount']

    def get_bid_offer_string(self):
        '''
        return display string for bid-offer spread string
        '''
        return f'B-{self.session_subject_period.session_subject.id_number} ${self.amount:0.2f}'

    #return json object of class
    def json(self):
        '''
        json object of model
        '''
        return{
            "id" : self.id
        }
        