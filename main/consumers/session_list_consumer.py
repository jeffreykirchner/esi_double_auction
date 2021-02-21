'''
websocket session list
'''
import json
import logging
import pytz

from channels.generic.websocket import AsyncWebsocketConsumer

from main.models import Session
from main.models import ParameterSet

from main.consumers import get_session_list_json
from main.consumers import create_new_session
from main.consumers import delete_session

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
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def create_session(self, event):
        '''
        create a new session
        '''
        logger = logging.getLogger(__name__) 
        logger.info(f"Create Session {event}")

        await create_new_session()
        
        #build response
        message_data = {}
        message_data["sessions"] = await get_session_list_json()

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

        #build response
        message_data = {}
        message_data["sessions"] = await get_session_list_json()

        message = {}
        message["messageType"] = event["type"]
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
