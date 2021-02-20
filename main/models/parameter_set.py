'''
sessions parameters
'''
from django.db import models
from django.db.utils import IntegrityError

from main.models import ConsentForms

import main

#experiment session parameters
class ParameterSet(models.Model):
    '''
    session parameters
    '''

    consent_form_required = models.BooleanField(default=True)                                               #true if subject must agree to special consent form before doing experiment
    consent_form = models.ForeignKey(ConsentForms,on_delete=models.CASCADE,null=True,blank=True)    #text of special consent form

    number_of_periods = models.IntegerField(default=1)                #number of periods in the session
    number_of_subjects = models.IntegerField(default=1)               #number of subjects in the session

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Study Parameter Set'
        verbose_name_plural = 'Study Parameter Sets'

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
            "consent_form_required" : self.consent_form_required,
            "consent_form" : self.consent_form.id if self.consent_form else None,
            "number_of_periods" : self.number_of_periods,
            "number_of_subjects" : self.number_of_subjects,
        }
