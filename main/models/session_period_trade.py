'''
session period trade model
'''

#import logging

from django.db import models

from . import SessionPeriod

class SessionPeriodTrade(models.Model):
    '''
    session period trade model
    '''
    session_period = models.ForeignKey(SessionPeriod, on_delete=models.CASCADE, related_name="session_period_trades")

    trade_number = models.IntegerField()

    timestamp = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['session_period', 'trade_number'], name='unique_SD_trade')
        ]
        ordering = ['trade_number']
        verbose_name = 'Session Period Trade'
        verbose_name_plural = 'Session Period Trades'

    #return json object of class
    def json(self):
        '''
        json object of model
        '''
        return{
            "id" : self.id
        }
        