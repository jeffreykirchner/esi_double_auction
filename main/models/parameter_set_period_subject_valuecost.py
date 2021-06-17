'''
subject parameters
'''
from django.db import models

from main.models import ParameterSetPeriodSubject

import main

class ParameterSetPeriodSubjectValuecost(models.Model):
    '''
    subject parameter value or cost
    '''
    parameter_set_period_subject = models.ForeignKey(ParameterSetPeriodSubject, on_delete=models.CASCADE, related_name="parameter_set_period_subject_valuecosts")

    value_cost = models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name = 'Value or Cost')    #value or cost
    enabled = models.BooleanField(default=True, verbose_name = 'Enabled')             #if true, use value or cost 

    timestamp = models.DateTimeField(auto_now_add = True)
    updated= models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Value or cost'
        verbose_name_plural = 'Value or costs'

    def from_dict(self, source):
        '''
        load values from source
        source : dict object representing this model
        '''

        self.value_cost = source.get("value_cost")
        self.enabled = True if source.get("enabled") == "True" else False

        self.save()

    def json(self):
        '''
        return json object of model
        '''
        return{

            "id" : self.id,
            "value_cost" : str(self.value_cost),
            "enabled" : "True" if self.enabled else "False",
            "label" : self.parameter_set_period_subject.get_label(),
        }
