'''
websocket session list
'''
import json
import logging

from main.consumers import SocketConsumerMixin
from main.consumers import get_session_list_json
from main.consumers import create_new_session
from main.consumers import delete_session

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
        logger.info(f"Get Sessions {event}")

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
