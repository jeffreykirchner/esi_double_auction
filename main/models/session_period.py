'''
session day model
'''

#import logging
import uuid

from django.db import models

from . import Session

class SessionPeriod(models.Model):
    '''
    session day model
    '''
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="session_periods")

    login_key = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name = 'Login Key')            #log in key used assign subjects by ID number
    period_number = models.IntegerField()

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['session', 'period_number'], name='unique_SD')
        ]
        verbose_name = 'Session Day'
        verbose_name_plural = 'Session Days'

    #return json object of class
    def json(self):
        '''
        json object of model
        '''
        return{
            "id" : self.id
        }
        