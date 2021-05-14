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

    number_of_periods = models.IntegerField(default=1, verbose_name="Number of periods")     #number of periods in the session
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

    def setup(self,new_ps):
        '''
        copy another parameter set into this one
        '''

        self.save()

        self.consent_form_required = new_ps.consent_form_required
        self.consent_form = new_ps.consent_form
        self.number_of_periods = new_ps.number_of_periods
        self.number_of_buyers = new_ps.number_of_buyers

        self.save()

    def add_parameter_set_subject(self, subject_type):
        '''
        create new parameter set subject set

        subject_type: SubjectType , BUYER or SELLER
        period_number: Int 1 to N
        id_number: Int unique ID within buyer or seller group, 1 to N
        '''

        last_subject = self.parameter_set_subjects.filter(subject_type=subject_type, period_number=1).last()

        if last_subject == None:
            id_number = 1
        else:
            id_number = last_subject.id_number + 1

        for period_number in range(self.number_of_periods):
            subject = main.models.ParameterSetSubject()

            subject.parameter_set = self
            subject.subject_type = subject_type
            subject.period_number = period_number + 1
            subject.id_number = id_number

            subject.save()

            for i in range(4):
                ps_value_cost = main.models.ParameterSetSubjectValuecost()

                ps_value_cost.parameter_set_subject = subject
                ps_value_cost.value_cost = 0

                ps_value_cost.save()

    def remove_parameter_set_subject(self, subject_type):
        '''
        remove the last parameter set subject

        create new parameter set subject
        parameter_set: ParameterSet to attach subject to
        subject_type: SubjectType , BUYER or SELLER
        period_number: Int 1 to N
        id_number: Int unique ID within buyer or seller group, 1 to N
        '''

        last_subject = self.parameter_set_subjects.filter(subject_type=subject_type, period_number=1).last()

        if last_subject == None:
            return "fail"

        self.parameter_set_subjects.filter(subject_type=subject_type, id_number=last_subject.id_number).delete()

        return "success"

    def json(self):
        '''
        return json object of model
        '''
        return{

            "id" : self.id,
            "consent_form_required" : self.consent_form_required,
            "consent_form" : self.consent_form.id if self.consent_form else None,
            "number_of_periods" : self.number_of_periods,
            "number_of_buyers" : self.number_of_buyers,
            "number_of_sellers" : self.number_of_sellers,
            "buyers" : [s.json()  for s in self.parameter_set_subjects.all() if s.subject_type == 'Buyer'],
            "sellers" : [s.json() for s in self.parameter_set_subjects.all() if s.subject_type == 'Seller'],
        }
