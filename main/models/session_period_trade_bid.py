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

    amount = models.IntegerField()

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = 'Session Period Trade Bid'
        verbose_name_plural = 'Session Period Trade Bids'

    #return json object of class
    def json(self):
        '''
        json object of model
        '''
        return{
            "id" : self.id
        }
        