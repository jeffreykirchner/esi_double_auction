import logging

from asgiref.sync import sync_to_async

from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from channels.db import database_sync_to_async


from main.models import Session, session

def user_is_owner(function):
    '''
    check if user is the creator of session or a super user
    '''
    def wrap(request, *args, **kwargs):      
        logger = logging.getLogger(__name__) 
        logger.info(f"user_is_owner {args} {kwargs}")

        try:
            session = Session.objects.get(id=kwargs['pk'])  
        except ObjectDoesNotExist :
            logger.warn(f"user_is_owner: Session not found")
            raise Http404('Session Not Found')
        
        if request.user == session.creator or \
           request.user.is_staff or \
           request.user in session.collaborators.all() :
           
            return function(request, *args, **kwargs)
        else:
            logger.warn(f"user_is_owner: Permisson denied")
            raise PermissionDenied

    return wrap

def user_is_super(function):
    '''
    check if user is a super user
    '''
    def wrap(request, *args, **kwargs):      
        
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap

def user_is_staff(function):
    '''
    check if user is a super user
    '''
    def wrap(request, *args, **kwargs):      
        
        if request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def check_sesison_exists_ws(function):

    async def wrap(self, *args, **kwargs):      
        logger = logging.getLogger(__name__) 
        logger.info(f"user_is_owner {args} {kwargs}")

        session_exists = await database_sync_to_async(get_session_exists)(args[0]["message_text"]["sessionID"])

        if session_exists:
            return await function(self, *args, **kwargs)
        else:
            logger.warning("check_sesison_exists_ws: session does not exist")
            return
    
    def get_session_exists(session_id):
        return Session.objects.filter(id=session_id).exists()

    return wrap

def check_user_is_owner_ws(function):
    '''
    check that user is creator of session or a super user.
    also check that session is valid
    '''
    async def wrap(self, *args, **kwargs):      
        logger = logging.getLogger(__name__) 
        logger.info(f"user_is_owner {args} {kwargs}")

        user_is_owner = await database_sync_to_async(check_user_is_owner)(self.scope['user'], args[0]["message_text"]["sessionID"])

        if user_is_owner:
            return await function(self, *args, **kwargs)
        else:
            logger.warning("check_user_is_owner_ws: invalid user")
            return
    
    def check_user_is_owner(user, session_id):
        logger = logging.getLogger(__name__) 

        try:
            session = Session.objects.get(id=session_id)  
        except ObjectDoesNotExist :
            logger.warn(f"check_user_is_owner_ws: Session not found")
            return False
        
        if user == session.creator or \
           user.is_staff or \
           user in session.collaborators.all() :
            return True
        else:
            return False
    
    return wrap

