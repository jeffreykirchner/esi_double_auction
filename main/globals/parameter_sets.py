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

    parameter_set.add_parameter_set_subject(SubjectType.BUYER, 1, 1)
    parameter_set.add_parameter_set_subject(SubjectType.SELLER, 1, 1)
    
    return parameter_set
