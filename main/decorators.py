import logging

from django.core.exceptions import PermissionDenied
from main.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


def user_is_owner(function):
    def wrap(request, *args, **kwargs):      
        logger = logging.getLogger(__name__) 
        logger.info(f"user_is_owner {args} {kwargs}")

        try:
            session = Session.objects.get(id=kwargs['pk'])  
        except ObjectDoesNotExist :
            logger.warn(f"user_is_owner: Session not found")
            raise Http404('Session Not Found')
        

        if request.user == session.creator or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            logger.warn(f"user_is_owner: Permisson denied")
            raise PermissionDenied

    return wrap

def user_is_super(function):
    def wrap(request, *args, **kwargs):      
        
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap