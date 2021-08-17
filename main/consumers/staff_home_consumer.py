'''
websocket session list
'''
from asgiref.sync import sync_to_async
from datetime import datetime

import json
import logging
import pytz

from django.core.serializers.json import DjangoJSONEncoder

from main.consumers import SocketConsumerMixin
from main.consumers import get_session_list_json
from main.consumers import delete_session

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

        message_text = event["message_text"]

        status = await delete_session(message_text["id"])

        logger.info(f"Delete Session success: {status}")

        #build response
        message_data = {}
        message_data["sessions"] = await get_session_list_json()

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

        await sync_to_async(create_new_session)(self.scope["user"])
        
        #build response
        message_data = {}
        message_data["sessions"] = await get_session_list_json()

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

        #build response
        message_data = {}
        message_data["sessions"] = await get_session_list_json()

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