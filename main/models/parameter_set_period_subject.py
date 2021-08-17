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

    def get_value_cost_list_json(self):
        '''
        return a list of values or costs associated with this subject in json format
        '''

        if self.subject_type == 'Buyer':
            return [v.json() for v in self.parameter_set_period_subject_valuecosts.all().order_by('-enabled', '-value_cost')]
        else:
            return [c.json() for c in self.parameter_set_period_subject_valuecosts.all().order_by('-enabled', 'value_cost')]
    
    def get_value_cost_list(self):
        '''
        return a list of values or costs models associated with this subject
        '''

        if self.subject_type == 'Buyer':
            return [v for v in self.parameter_set_period_subject_valuecosts.all().order_by('-enabled', '-value_cost')]
        else:
            return [c for c in self.parameter_set_period_subject_valuecosts.all().order_by('-enabled', 'value_cost')]

    def add_to_values_or_costs(self, amount):
        '''
        add to all values or costs in the amount specficied
        value_or_cost : string 'value' or 'cost'
        amount: decimal
        '''

        for i in self.get_value_cost_list():
            i.value_cost += amount

            if i.value_cost < 0:
                i.value_cost = 0

            i.save()
        
        return "success"

    def from_dict(self, source):
        '''
        load values from dict
        '''

        message = "Parameters loaded successfully."

        # try:
        # self.parameter_set_period = main.models.ParameterSet.objects.get(id=source.get("parameter_set_period"))
        self.subject_type = source.get("subject_type")
        self.id_number = source.get("id_number")

        value_cost_list = self.get_value_cost_list()

        for i in range(len(value_cost_list)):
            value_cost_list[i].from_dict(source.get("value_costs")[i])

        self.save()

        # except IntegrityError as exp:
        #     message = f"Failed to load parameter set subject: {exp}"
        #     #logger.info(message)

        return message

    def get_label(self):
        '''
        return label display string
        '''

        if self.subject_type == 'Buyer':
            return f'B{self.id_number}'
        else:
            return f'S{self.id_number}'


    def json(self):
        '''
        return json object of model
        '''

        return{

            "id" : self.id,
            # "parameter_set_period" : self.parameter_set_period.id,
            "id_number" : self.id_number,
            "subject_type" : self.subject_type,
            "value_costs" : self.get_value_cost_list_json(),
        }
