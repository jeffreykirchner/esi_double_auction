'''
a value or cost for a subject in a period
'''
from django.db import models

from main.models import ParameterSetPeriodSubject

#experiment session parameters
class ParameterSetPeriodSubjectValuecost(models.Model):
    '''
    a value or cost for a subject in a period
    '''

    parameter_set_period_subject = models.ForeignKey(ParameterSetPeriodSubject, on_delete=models.CASCADE,
                                                     related_name="parameter_set_period_subject_values")

    value_cost = models.DecimalField(decimal_places=2, max_digits=4, default=5)

    timestamp = models.DateTimeField(auto_now_add = True)
    updated= models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Parameter Set Subject Value or Cost'
        verbose_name_plural = 'Parameter Sets Subjet Value or Costs'

    def json(self):
        '''
        return json object of model
        '''
        return{

            "id" : self.id,
            "value_cost" : float(self.value_cost),
        }
