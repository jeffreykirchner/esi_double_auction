'''
session's period parameters
'''
from django.db import models
from django.db.utils import IntegrityError

from main.models import ParameterSet

import main

#experiment session parameters
class ParameterSetPeriod(models.Model):
    '''
    session single period parameters 
    '''

    parameter_set = models.ForeignKey(ParameterSet, on_delete=models.CASCADE,  related_name="parameter_set_periods")

    period_number = models.IntegerField(verbose_name='Period number')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Period Parameter Set'
        verbose_name_plural = 'Period Parameter Sets'
        ordering = ['period_number']
        constraints = [
            models.UniqueConstraint(fields=['parameter_set', 'period_number'], name='unique_period'),
        ]

    def update_subject_count(self):
        '''
        create new parameter set subject set

        subject_type: SubjectType , BUYER or SELLER
        period_number: Int 1 to N
        id_number: Int unique ID within buyer or seller group, 1 to N
        '''

        #remove extra buyers
        buyers_excess = self.parameter_set_period_subjects.filter(subject_type=main.globals.SubjectType.BUYER,
                                                                  id_number__gt = self.parameter_set.number_of_buyers)

        if buyers_excess != None:
            buyers_excess.delete()


        #remove extra sellers
        sellers_excess = self.parameter_set_period_subjects.filter(subject_type=main.globals.SubjectType.SELLER,
                                                                  id_number__gt = self.parameter_set.number_of_sellers)

        if sellers_excess != None:
            sellers_excess.delete()

        #add needed buyers
        current_buyer_count = self.parameter_set_period_subjects.filter(subject_type=main.globals.SubjectType.BUYER)

        for i in range(current_buyer_count.count() + 1, self.parameter_set.number_of_buyers+1):
            subject = main.models.ParameterSetPeriodSubject()

            subject.parameter_set_period = self
            subject.subject_type = main.globals.SubjectType.BUYER
            subject.id_number = i

            subject.save()

            for i in range(4):
                ps_value_cost = main.models.ParameterSetPeriodSubjectValuecost()

                ps_value_cost.parameter_set_period_subject = subject
                ps_value_cost.value_cost = 0

                ps_value_cost.save()
        
        #add needed sellers
        current_seller_count = self.parameter_set_period_subjects.filter(subject_type=main.globals.SubjectType.SELLER)

        for i in range(current_seller_count.count() + 1, self.parameter_set.number_of_sellers+1):
            subject = main.models.ParameterSetPeriodSubject()

            subject.parameter_set_period = self
            subject.subject_type = main.globals.SubjectType.SELLER
            subject.id_number = i

            subject.save()

            for i in range(4):
                ps_value_cost = main.models.ParameterSetPeriodSubjectValuecost()

                ps_value_cost.parameter_set_period_subject = subject
                ps_value_cost.value_cost = 0

                ps_value_cost.save()

        return "success"

        # last_subject = self.parameter_set_period_subjects.filter(subject_type=subject_type).last()

        # if last_subject == None:
        #     id_number = 1
        # else:
        #     id_number = last_subject.id_number + 1

        # # for period_number in range(self.parameter_set.number_of_periods):
        # subject = main.models.ParameterSetPeriodSubject()

        # subject.parameter_set_period = self
        # subject.subject_type = subject_type
        # subject.id_number = id_number

        # subject.save()

        # for i in range(4):
        #     ps_value_cost = main.models.ParameterSetPeriodSubjectValuecost()

        #     ps_value_cost.parameter_set_period_subject = subject
        #     ps_value_cost.value_cost = 0

        #     ps_value_cost.save()

    def remove_parameter_set_subject(self, subject_type):
        '''
        remove the last parameter set subject

        create new parameter set subject
        parameter_set: ParameterSet to attach subject to
        subject_type: SubjectType , BUYER or SELLER
        period_number: Int 1 to N
        id_number: Int unique ID within buyer or seller group, 1 to N
        '''

        last_subject = self.parameter_set_period_subjects.filter(subject_type=subject_type).last()

        if last_subject == None:
            return "fail"

        self.parameter_set_period_subjects.filter(subject_type=subject_type, id_number=last_subject.id_number).delete()

        return "success"

    def json(self):
        '''
        return json object of model
        '''
        return{

            "id" : self.id,
            "period_number" : self.period_number,
            "buyers" : [s.json()  for s in self.parameter_set_period_subjects.all() if s.subject_type == 'Buyer'],
            "sellers" : [s.json() for s in self.parameter_set_period_subjects.all() if s.subject_type == 'Seller'],
        }
