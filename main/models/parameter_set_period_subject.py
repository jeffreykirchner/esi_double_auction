'''
sessions parameters
'''
from django.db import models
from django.db.utils import IntegrityError
from django.utils.translation import gettext_lazy as _

from main.models import ParameterSetPeriod

import main

#experiment session parameters
class ParameterSetPeriodSubject(models.Model):
    '''
    session parameters
    '''

    class SubjectType(models.TextChoices):
        '''
        Subject Type
        '''
        BUYER = 'Buyer', _('Buyer')          #buy only
        SELLER = "Seller", _('Seller')       #sell only

    parameter_set_period = models.ForeignKey(ParameterSetPeriod,on_delete=models.CASCADE, related_name="parameter_set_period_subjects")

    id_number = models.IntegerField(default=1, verbose_name='ID Number in Session')                         #local id number in session
    subject_type = models.CharField(default=SubjectType.BUYER, max_length=100,
                                    choices=SubjectType.choices, verbose_name="Type of participant")        #type of participant

    timestamp = models.DateTimeField(auto_now_add = True)
    updated= models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Study Parameter Set Subject'
        verbose_name_plural = 'Study Parameter Sets Subjets'

        constraints = [
            models.UniqueConstraint(fields=['parameter_set_period', 'id_number'], name='unique_PSPS')
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
            "id_number" : self.id_number,
            "subject_type" : self.subject_type,
            "inventory" : self.inventory,
            "values" : [value.json() for value in self.parameter_set_period_subject_values.all()]
        }
