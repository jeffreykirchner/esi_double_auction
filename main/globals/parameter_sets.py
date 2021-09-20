'''
gloabal functions related to parameter sets
'''

from django.db import models
from django.utils.translation import gettext_lazy as _

import main

class SubjectType(models.TextChoices):
    '''
    subject types for parameter sets
    '''
    BUYER = 'Buyer', _('Buyer')
    SELLER = 'Seller', _('Seller')

class PriceCapType(models.TextChoices):
    '''
    Price cap types for parameter sets
    '''
    FLOOR = 'Floor', _('Floor')
    CEILING = 'Ceiling', _('Ceiling')

def create_new_session_parameterset():
    '''
    create new parameter set
    '''

    parameter_set = main.models.ParameterSet()
    parameter_set.save()

    parameter_set.add_session_period()
    
    return parameter_set
