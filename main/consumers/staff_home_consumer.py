'''
websocket session list
'''
from asgiref.sync import sync_to_async
from datetime import datetime
from asgiref.sync import sync_to_async

import json
import logging
import pytz

from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from main.consumers import SocketConsumerMixin

from main.models import Session
from main.globals import create_new_session_parameterset

class StaffHomeConsumer(SocketConsumerMixin):
    '''
    websocket session list
    '''    
    
    async def delete_session(self, event):
        '''
        delete specified session
        '''
        logger = logging.getLogger(__name__) 
        logger.info(f"Delete Session {event}")

        self.user = self.scope["user"]
        logger.info(f"User {self.user}")

        message_text = event["message_text"]

        status = await delete_session(message_text["id"])

        logger.info(f"Delete Session success: {status}")

        #build response
        message_data = {}
        message_data["sessions"] = await sync_to_async(get_session_list_json)(self.user)

        message = {}
        message["messageType"] = "get_sessions"
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message,}, cls=DjangoJSONEncoder))

    async def create_session(self, event):
        '''
        create a new session
        '''
        logger = logging.getLogger(__name__) 
        logger.info(f"Create Session {event}")

        self.user = self.scope["user"]
        logger.info(f"User {self.user}")

        await sync_to_async(create_new_session)(self.user)
        
        #build response
        message_data = {}
        message_data["sessions"] = await sync_to_async(get_session_list_json)(self.user)

        message = {}
        message["messageType"] = event["type"]
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message,}, cls=DjangoJSONEncoder))
    
    async def get_sessions(self, event):
        '''
        return a list of sessions
        '''
        logger = logging.getLogger(__name__) 
        logger.info(f"Get Sessions {event}")   

        self.user = self.scope["user"]
        logger.info(f"User {self.user}")     

        #build response
        message_data = {}
        message_data["sessions"] = await sync_to_async(get_session_list_json)(self.user)

        message = {}
        message["messageType"] = event["type"]
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message,}, cls=DjangoJSONEncoder))


def create_new_session(auth_user):
    '''
    create an emtpy session and return it
    '''
    
    session = Session()

    session.parameter_set = create_new_session_parameterset()
    session.start_date = datetime.now(pytz.UTC)
    session.creator = auth_user

    session.save()

    logger = logging.getLogger(__name__) 
    logger.info(f"Create New Session {session}")

    return session


def get_session_list_json(usr):
    '''
    get list of sessions
    '''
    return [{"title" : i.title,
             "id":i.id,
             "locked":i.locked,
             "start_date":i.get_start_date_string(),
            }
            for i in Session.objects.filter(soft_delete=False, creator=usr)]

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
        return session.json()
    except ObjectDoesNotExist:
        logger.warning(f"get_session session, not found: {id_}")
        return {}
    