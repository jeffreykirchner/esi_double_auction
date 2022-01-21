'''
session subject model
'''

from django.db import models

from main.models import SessionSubject
from main.models import SessionPeriod
from main.models import ParameterSetPeriodSubject

#subject in session
class SessionSubjectPeriod(models.Model):
    '''
    session subject period model
    '''
    session_subject = models.ForeignKey(SessionSubject, on_delete=models.CASCADE, related_name="session_subject_periods_a")
    session_period = models.ForeignKey(SessionPeriod, on_delete=models.CASCADE, related_name="session_subject_periods_b")
    parameter_set_period_subject = models.ForeignKey(ParameterSetPeriodSubject, on_delete=models.CASCADE, related_name="session_subject_periods_c")
   
    current_unit_number = models.IntegerField(default=1)       #current unit in the parameter set subject is trading
    
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['session_subject', 'session_period'], name='Session_subject_period')
        ]
        verbose_name = 'Session Subject Period'
        verbose_name_plural = 'Session Subject Periods'
    
    def get_current_value_cost(self):
        '''
        return the current value or cost
        '''
        return self.get_value_cost(self.current_unit_number-1)
        
    
    def get_value_cost(self, index):
        '''
        return the ParameterSetPeriodSubjectValuecost at index
        '''
        if index >= 4:
            return None
        
        value_cost = self.parameter_set_period_subject.get_value_cost_list()[index]

        if not value_cost.enabled:
            return None

        return value_cost

    #return json object of class
    def json(self):
        '''
        json object of model
        '''

        return {
            "id" : self.id,
            "name" : self.name,
            "contact_email" : self.contact_email,
            "student_id" : self.student_id,
            "consent_required" : self.consent_required,
            "questionnaire1_required" : self.questionnaire1_required,
            "questionnaire2_required" : self.questionnaire2_required,
        }
