'''
gloabal functions related to parameter sets
'''

from django.db import models
from django.utils.translation import gettext_lazy as _

import main

class SubjectType(models.TextChoices):
    '''
    treatment types for session
    '''
    BUYER = 'Buyer', _('Buyer')
    SELLER = 'Seller', _('Seller')

def create_new_session_parameterset():
    '''
    create new parameter set
    '''

    parameter_set = main.models.ParameterSet()
    parameter_set.save()

    add_parameter_set_subject(parameter_set, SubjectType.BUYER, 1, 1)
    add_parameter_set_subject(parameter_set, SubjectType.SELLER, 1, 1)
    
    return parameter_set

def add_parameter_set_subject(parameter_set, subject_type, period_number, id_number):
    '''
    create new parameter set subject
    '''

    subject = main.models.ParameterSetSubject()

    subject.parameter_set = parameter_set
    subject.subject_type = subject_type
    subject.period_number = period_number
    subject.id_number = id_number

    subject.save()

    for i in range(4):
        ps_value_cost = main.models.ParameterSetSubjectValuecost()

        ps_value_cost.parameter_set_subject = subject
        ps_value_cost.value_cost = 0

        ps_value_cost.save()
