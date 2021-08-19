from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.shortcuts import render
from main.models import Session
import logging

def user_is_owner(function):
    def wrap(request, *args, **kwargs):      
        logger = logging.getLogger(__name__) 
        logger.info(f"user_is_owner {args} {kwargs}")

        session = Session.objects.get(id=kwargs['pk'])

        if request.user == session.creator:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap