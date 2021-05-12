'''
subject parameters
'''
from django.db import models

from main.models import ParameterSetSubject

import main

class ParameterSetSubjectValuecost(models.Model):
    '''
    subject parameter value or cost
    '''
    parameter_set_subject = models.ForeignKey(ParameterSetSubject, on_delete=models.CASCADE, related_name="parameter_set_subject_valuecosts")

    value_cost = models.DecimalField(decimal_places=2, default=0, max_digits=5)    #value or cost

    timestamp = models.DateTimeField(auto_now_add = True)
    updated= models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Value or cost'
        verbose_name_plural = 'Value or costs'

    def json(self):
        '''
        return json object of model
        '''
        return{

            "id" : self.id,
            "value_cost" : str(self.value_cost),
        }
