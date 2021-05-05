'''
static snyc_to_async methods
'''
from datetime import datetime

import pytz
import logging

from asgiref.sync import sync_to_async

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from main.models import Session
from main.models import ParameterSet

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

    parameter_set = ParameterSet()
    parameter_set.save()

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

@sync_to_async
def get_session(id_):
    '''
    return session with specified id
    param: id_ {int} session id
    '''
    session = None
    logger = logging.getLogger(__name__)

    try:        
        session = Session.objects.get(id=id_)
    except ObjectDoesNotExist:
        logger.warning(f"get_session session, not found: {id_}")
    
    return session.json()
        

