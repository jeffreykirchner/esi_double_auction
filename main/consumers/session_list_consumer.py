'''
websocket session list
'''
from datetime import datetime

import json
import logging
import pytz

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

from main.models import Session
from main.models import ParameterSet

class SessionListConsumer(AsyncWebsocketConsumer):
    '''
    websocket session list
    '''
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

     # Receive message from WebSocket
    async def receive(self, text_data):
        '''
        incoming data from websocket
        '''
        text_data_json = json.loads(text_data)

        message_type = text_data_json['messageType']
        message_text = text_data_json['messageText']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': message_type,
                'message_text': message_text
            }
        )

    async def create_session(self, event):
        '''
        create a new session
        '''
        logger = logging.getLogger(__name__) 
        logger.info(f"Create Session {event}")

        parameter_set = ParameterSet()
        parameter_set.save()

        session = Session()

        session.parameter_set = parameter_set
        session.start_date = datetime.now(pytz.UTC)

        session.save()
        
        message_data = {}
        message_data["sessions"] = [i.json() for i in Session.objects.all()]

        message = {}
        message["messageType"] = event["type"]
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
    
    async def get_sessions(self, event):
        '''
        return a list of sessions
        '''
        logger = logging.getLogger(__name__) 
        logger.info(f"Get Session {event}")

        message_data = {}
        message_data["sessions"] = await self.get_session_list_json()

        message = {}
        message["messageType"] = event["type"]
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @sync_to_async
    def get_session_list_json(self):

        return [i.json() for i in Session.objects.all()]
