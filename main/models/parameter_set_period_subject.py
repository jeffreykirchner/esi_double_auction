'''
subject parameters
'''
from django.db import models
from django.db.utils import IntegrityError

from main.models import ParameterSetPeriod
from main.globals import SubjectType

import main

class ParameterSetPeriodSubject(models.Model):
    '''
    subject parameters
    '''

    parameter_set_period = models.ForeignKey(ParameterSetPeriod, on_delete=models.CASCADE, related_name="parameter_set_period_subjects")

    id_number = models.IntegerField(verbose_name='ID Number in Period')                                #local id number in the period
    subject_type = models.CharField(max_length=100, choices=SubjectType.choices, default=SubjectType.BUYER)         #subject type of subject

    timestamp = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Parameters for Subject'
        verbose_name_plural = 'Parameters for Subjects'
        ordering = ['subject_type', 'id_number']
        constraints = [
            models.UniqueConstraint(fields=['parameter_set_period', 'id_number', 'subject_type'], name='unique_subject_for_period'),
        ]

    def setup_from_dict(self, new_ps):
        '''
        load values from dict
        '''

        message = "Parameters loaded successfully."

        try:
            self.parameter_set = main.models.ParameterSet.objects.get(id=new_ps.get("parameter_set"))
            self.id_number = new_ps.get("id_number")

            self.save()

        except IntegrityError as exp:
            message = f"Failed to load parameter set subject: {exp}"
            #logger.info(message)

        return message

    def setup(self,new_ps):
        '''
        copy another parameter set into this one
        '''

        self.save()

        self.parameter_set = new_ps.parameter_set
        self.id_number = new_ps.id_number

        self.save()

    def json(self):
        '''
        return json object of model
        '''

        if self.subject_type == 'Buyer':
            value_costs = [vc.json() for vc in self.parameter_set_period_subject_valuecosts.all().order_by('-enabled', '-value_cost')]
        else:
            value_costs = [vc.json() for vc in self.parameter_set_period_subject_valuecosts.all().order_by('-enabled', 'value_cost')]

        return{

            "id" : self.id,
            "id_number" : self.id_number,
            "subject_type" : self.subject_type,
            "value_costs" : value_costs,
        }
