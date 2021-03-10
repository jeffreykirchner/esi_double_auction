'''
sessions parameter period
'''
from django.db import models
from django.db.utils import IntegrityError

from main.models import ParameterSet

import main

#experiment session parameters
class ParameterSetPeriod(models.Model):
    '''
    session parameter period
    '''
    parameter_set = models.ForeignKey(ParameterSet, on_delete=models.CASCADE, related_name="parameter_set_periods")
  
    number = models.IntegerField(default=1, verbose_name= "Period Number")             #period number in set

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Parameter Set Period'
        verbose_name_plural = 'Parameter Set Periods'

        constraints = [
            models.UniqueConstraint(fields=['parameter_set', 'number'], name='unique_PSP')
        ]

    def setup_from_dict(self, new_ps):
        '''
        load values from dict
        '''

        message = "Parameters loaded successfully."

        try:
            self.consent_form_required = new_ps.get("consent_form_required")
            self.consent_form = main.models.ConsentForms.objects.get(id=new_ps.get("consent_form"))
            self.number_of_periods = new_ps.get("number_of_periods")
            self.number_of_subjects = new_ps.get("number_of_subjects")

            self.save()

        except IntegrityError as exp:
            message = f"Failed to load parameter set: {exp}"
            #logger.info(message)

        return message

    def setup(self,new_ps):
        '''
        copy another parameter set into this one
        '''

        self.save()

        self.consent_form_required = new_ps.consent_form_required
        self.consent_form = new_ps.consent_form
        self.number_of_periods = new_ps.number_of_periods
        self.number_of_subjects = new_ps.number_of_subjects

        self.save()

    def json(self):
        '''
        return json object of model
        '''
        return{

            "id" : self.id,
            "number" : self.number,
            "subjects" : [subject.json() for subject in self.parameter_set_period_subjects.all()],
        }
