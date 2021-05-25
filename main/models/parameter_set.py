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

    consent_form_required = models.BooleanField(default=True)                                          #true if subject must agree to special consent form before doing experiment
    consent_form = models.ForeignKey(ConsentForms, on_delete=models.CASCADE, null=True, blank=True)       #text of special consent form

    number_of_buyers = models.IntegerField(default=1, verbose_name="Number of buyers")       #number of buyers in the session
    number_of_sellers = models.IntegerField(default=1, verbose_name="Number of sellers")     #number of buyers in the session

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
            self.number_of_buyers = new_ps.get("number_of_buyers")

            self.save()

        except IntegrityError as exp:
            message = f"Failed to load parameter set: {exp}"
            #logger.info(message)

        return message

    def setup(self, new_ps):
        '''
        copy another parameter set into this one
        '''

        self.save()

        self.consent_form_required = new_ps.consent_form_required
        self.consent_form = new_ps.consent_form
        self.number_of_periods = new_ps.number_of_periods
        self.number_of_buyers = new_ps.number_of_buyers

        self.save()

    def add_session_period(self):
        '''
        add new period to session
        '''

        last_period = self.parameter_set_periods.last()

        if last_period == None:
            period_number = 1
        else:
            period_number = last_period.period_number + 1

        parameter_set_period = main.models.ParameterSetPeriod()

        parameter_set_period.parameter_set = self
        parameter_set_period.period_number = period_number

        parameter_set_period.save()

        parameter_set_period.update_subject_count()

        return "success"
    
    def remove_session_period(self):
        '''
        remove last period froms session
        '''

        last_period = self.parameter_set_periods.last()

        if last_period == None:
            return "fail"
        
        if last_period.period_number <= 1:
            return "fail"
        
        last_period.delete()

        return "success"
    
    def update_subject_counts(self):
        '''
        update the number of subjects in the session
        '''

        status = "success"

        for i in self.parameter_set_periods.all():
            if i.update_subject_count() == "fail":
                status = "fail"

        return status
    
    def shift_values_or_costs(self, value_or_cost, period_number, direction):
        '''
        shift the values or costs for a period in the direction specified
        value_or_cost : string 'value' or 'cost'
        period : int 1 to N
        direction: string 'up' or 'down'
        '''

        parameter_set_period = self.parameter_set_periods.get(period_number = period_number)

        return parameter_set_period.shift_values_or_costs(value_or_cost, direction)

    def json(self):
        '''
        return json object of model
        '''
        return{

            "id" : self.id,
            "consent_form_required" : self.consent_form_required,
            "consent_form" : self.consent_form.id if self.consent_form else None,
            "number_of_periods" : self.parameter_set_periods.all().count(),
            "number_of_buyers" : self.number_of_buyers,
            "number_of_sellers" : self.number_of_sellers,
            "periods" : [p.json()  for p in self.parameter_set_periods.all()],
        }
