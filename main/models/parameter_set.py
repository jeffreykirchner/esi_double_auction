'''
sessions parameters
'''
from django.db import models
from django.db.utils import IntegrityError

from main.models import ConsentForms

import main
import main.models

#experiment session parameters
class ParameterSet(models.Model):
    '''
    session parameters
    '''
    consent_form_required = models.BooleanField(default=True)                                           #true if subject must agree to special consent form before doing experiment
    consent_form = models.ForeignKey(ConsentForms,on_delete=models.CASCADE,null=True,blank=True)        #text of special consent form

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Experiment Parameter Set'
        verbose_name_plural = 'Experiment Parameter Sets'

    def setup_from_dict(self, new_ps):
        '''
        load values from dict
        '''

        message = "Parameters loaded successfully."

        try:
            self.consent_form_required = new_ps.get("consent_form_required")
            self.consent_form = main.models.ConsentForms.objects.get(id=new_ps.get("consent_form"))

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

        self.save()
    
    def add_period(self):
        '''
        add a new period to parameter set
        '''

        last_parameter_set_period = self.parameter_set_periods.all().last()

        parameter_set_period = main.models.ParameterSetPeriod()
        parameter_set_period.number = last_parameter_set_period.number + 1
        parameter_set_period.parameter_set = self
        parameter_set_period.save()
    
    def get_period_count(self):
        '''
        return the number of periods
        '''
        return self.parameter_set_periods.all().count()

    def json(self):
        '''
        return json object of model
        '''
        return{
            "id" : self.id,
            "consent_form_required" : self.consent_form_required,
            "consent_form" : self.consent_form.id if self.consent_form else None,
            "periods" : [psp.json() for psp in self.parameter_set_periods.all()],
        }
