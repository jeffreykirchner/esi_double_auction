'''
session period trade model
'''

#import logging

from django.db import models

from . import SessionPeriod
# from . import SessionSubjectPeriod
# from . import ParameterSetPeriodSubjectValuecost

import main

class SessionPeriodTrade(models.Model):
    '''
    session period trade model
    '''
    session_period = models.ForeignKey(SessionPeriod, on_delete=models.CASCADE, related_name="session_period_trades_a")

    trade_number = models.IntegerField()                     #numbered from one to N
    trade_complete = models.BooleanField(default=False)      #true once a trade is complete
    trade_price = models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Trade Price')         #price that trade was completed at

    buyer = models.ForeignKey('main.SessionSubjectPeriod', on_delete=models.CASCADE, related_name="session_period_trades_b", blank=True, null=True)
    buyer_value = models.ForeignKey('main.ParameterSetPeriodSubjectValuecost', on_delete=models.CASCADE, related_name="session_period_trades_c", blank=True, null=True)

    seller = models.ForeignKey('main.SessionSubjectPeriod', on_delete=models.CASCADE, related_name="session_period_trades_d", blank=True, null=True)
    seller_cost = models.ForeignKey('main.ParameterSetPeriodSubjectValuecost', on_delete=models.CASCADE, related_name="session_period_trades_e", blank=True, null=True)

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
    
    def get_best_bid(self):
        '''
        return the best bid
        '''
        return self.session_period_trade_bids.order_by('amount').last()

    def get_best_offer(self):
        '''
        return the best offer
        '''
        return self.session_period_trade_offers.order_by('-amount').last()
    
    def get_total_gains_from_trade(self):
        '''
        return the gains from this trade
        '''
        
        if not self.trade_complete:
            return 0
        
        total_gains = self.buyer_value.value_cost - self.trade_price
        total_gains += self.trade_price - self.seller_cost.value_cost

        return total_gains


    #return json object of class
    def json(self):
        '''
        json object of model
        '''
        return{
            "id" : self.id
        }
        