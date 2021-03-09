'''
static snyc_to_async methods
'''
from datetime import datetime

import logging
import pytz

from asgiref.sync import sync_to_async

from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from main.models import Session
from main.models import ParameterSet
from main.models import ParameterSetPeriod
from main.models import ParameterSetPeriodSubject
from main.models import ParameterSetPeriodSubjectValuecost

@sync_to_async
def get_session_list_json():
    '''
    get list of sessions
    '''
    return [i.json() for i in Session.objects.filter(soft_delete=False)]

@sync_to_async
def create_new_session():
    '''
    create an emtpy session and return it
    '''

    #create new parameter set
    parameter_set = ParameterSet()
    parameter_set.save()

    parameter_set_period = ParameterSetPeriod()
    parameter_set_period.parameter_set = parameter_set
    parameter_set_period.save()

    #setup seller
    parameter_set_period_subject_1 = ParameterSetPeriodSubject()
    parameter_set_period_subject_1.id_number = 1
    parameter_set_period_subject_1.SubjectType = "Seller"
    parameter_set_period_subject_1.save()

    #setup buyer
    parameter_set_period_subject_2 = ParameterSetPeriodSubject()
    parameter_set_period_subject_2.id_number = 2
    parameter_set_period_subject_2.SubjectType = "Buyer"
    parameter_set_period_subject_2.save()

    #seller costs
    valuecost_1 = ParameterSetPeriodSubjectValuecost()
    valuecost_1.parameter_set_period_subject = parameter_set_period_subject_1
    valuecost_1.value_cost = 2
    valuecost_1.save()

    valuecost_2 = ParameterSetPeriodSubjectValuecost()
    valuecost_2.parameter_set_period_subject = parameter_set_period_subject_1
    valuecost_2.value_cost = 4
    valuecost_2.save()

    #buyer values
    valuecost_3 = ParameterSetPeriodSubjectValuecost()
    valuecost_3.parameter_set_period_subject = parameter_set_period_subject_2
    valuecost_3.value_cost = 6
    valuecost_3.save()

    valuecost_4 = ParameterSetPeriodSubjectValuecost()
    valuecost_4.parameter_set_period_subject = parameter_set_period_subject_2
    valuecost_4.value_cost = 8
    valuecost_4.save()

    #create new session
    session = Session()

    session.parameter_set = parameter_set
    session.start_date = datetime.now(pytz.UTC)

    session.save()

    logger = logging.getLogger(__name__) 
    logger.info(f"Create New Session {session}")

    return session

@sync_to_async
def delete_session(id_):
    '''
    delete specified session
    param: id_ {int} session id
    '''

    logger = logging.getLogger(__name__)   

    try:
        session = Session.objects.get(id=id_)

        if settings.DEBUG:
            session.delete()
        else:
            session.soft_delete=True
            session.save()

        logger.info(f"Delete Session {id_}")
        return True
    except ObjectDoesNotExist:
        logger.warning(f"Delete Session, not found: {id}")
        return False

# @sync_to_async
# def get_session(id_):
#     '''
#     return session with specified id
#     param: id_ {int} session id
#     '''

#     try:        
#         return Session.objects.get(id=id_).json()
#     except ObjectDoesNotExist:
#         logger = logging.getLogger(__name__)
#         logger.warning(f"get_session session, not found: {id_}")
#         return {}
    
@sync_to_async
def get_model_json(id_ : int, model : models.Model):
    '''
    return the parameter set with specified id
    param: id_ {int} parameter set id
    '''

    try:        
        return model.objects.get(id=id_).json()
    except ObjectDoesNotExist:
        logger = logging.getLogger(__name__)
        logger.warning(f"get model json: {model}, not found: {id_}")
        return {}