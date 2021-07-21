'''
session period model
'''

#import logging

from django.db import models

from . import Session

import main

class SessionPeriod(models.Model):
    '''
    session period model
    '''
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="session_periods")

    period_number = models.IntegerField()                       #period number from 1 to N
    current_trade_number = models.IntegerField(default=1)       #current trade number in the period 

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['session', 'period_number'], name='unique_SD')
        ]
        verbose_name = 'Session Period'
        verbose_name_plural = 'Session Periods'
        ordering = ['period_number']

    def get_bid_list_json(self):
        '''
        return a list of bids for this period in json format
        '''
        return list(main.models.SessionPeriodTradeBid.objects.filter(session_period_trade__in=self.session_period_trades_a.all())
                                                             .values('amount', 'session_period_trade__trade_number')
                                                             .order_by('session_period_trade__trade_number', 'amount'))

    def get_offer_list_json(self):
        '''
        return a list of offers for this period in json format
        '''
        return list(main.models.SessionPeriodTradeOffer.objects.filter(session_period_trade__in=self.session_period_trades_a.all())
                                                               .values('amount', 'session_period_trade__trade_number')
                                                               .order_by('session_period_trade__trade_number', '-amount'))

    def get_current_best_bid(self):
        '''
        return the best bid from the current trade
        '''        
        return self.get_current_trade().get_best_bid()

    def get_current_best_offer(self):
        '''
        return the best offer from the current trade
        '''        
        return self.get_current_trade().get_best_offer()

    def get_current_trade(self):
        '''
        return the current trade
        '''
        return self.session_period_trades_a.get(trade_number=self.current_trade_number)

    def get_trade_list_json(self):
        '''
        return a list if completed trades
        '''
        return list(self.session_period_trades_a.filter(trade_complete=True)
                                                .values('id', 'trade_price', 'buyer__session_subject__id_number', 'seller__session_subject__id_number')
                                                .order_by('trade_number'))

    #return json object of class
    def json(self):
        '''
        json object of model
        '''
        #current_best_bid = self.get_current_best_bid()
        #current_best_offer = self.get_current_best_offer()

        #current_trade = self.get_current_trade()

        return{
            "id" : self.id,
            "current_trade_number" : self.current_trade_number,
            "bid_list" : self.get_bid_list_json(),
            "offer_list" : self.get_offer_list_json(),
            "trade_list" : self.get_trade_list_json(),
            "current_best_bid" : i.get_bid_offer_string() if (i:=self.get_current_best_bid()) else "---",
            "current_best_offer" : i.get_bid_offer_string() if (i:=self.get_current_best_offer()) else "---",
        }
        