'''
subject parameters
'''
from django.db import models
from django.db.utils import IntegrityError
from django.utils.translation import gettext_lazy as _

from main.models import ParameterSet

import main

class ParameterSetSubject(models.Model):
    '''
    subject parameters
    '''

    class SubjectType(models.TextChoices):
        '''
        treatment types for session
        '''
        BUYER = 'Buyer', _('Buyer')
        SELLER = 'Seller', _('Seller')

    parameter_set = models.ForeignKey(ParameterSet,on_delete=models.CASCADE, related_name="parameter_set_subjects")

    period_number = models.IntegerField(null=True, verbose_name = 'Period number')
    id_number = models.IntegerField(null=True, verbose_name = 'ID Number in Period')                                #local id number in the period
    subject_type = models.CharField(max_length=100, choices=SubjectType.choices, default=SubjectType.BUYER)         #subject type of subject

    timestamp = models.DateTimeField(auto_now_add = True)
    updated= models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Parameters for Subject'
        verbose_name_plural = 'Parameters for Subjects'

        constraints = [
            models.UniqueConstraint(fields=['parameter_set', 'period_number', 'id_number', 'subject_type'], name='unique_subject_for_period'),
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
        return{

            "id" : self.id,
            "period_number" : self.period_number,
            "id_number" : self.id_number,
            "subject_type" : self.subject_type,
            "value_costs" : [vc.json() for vc in self.parameter_set_subject_valuecosts.all()]
        }
