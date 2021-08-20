'''
websocket session list
'''
from asgiref.sync import sync_to_async

import json
import logging

from django.core.serializers.json import DjangoJSONEncoder

from main.consumers import SocketConsumerMixin


class StaffAdminToolsConsumer(SocketConsumerMixin):
    '''
    websocket admin tools
    '''    
    
    async def upload_parameters(self, event):
        '''
        upload legacy parameter file
        '''
        logger = logging.getLogger(__name__) 
        logger.info(f"Upload Legacy parameter file {event}")

        self.user = self.scope["user"]
        logger.info(f"User {self.user}")

        message_text = event["message_text"]

        #build response
        message_data = {}
        message_data["result"] = await sync_to_async(upload_parameter_file)(message_text["ini_text"], self.user)

        message = {}
        message["messageType"] = event["type"]
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message,}, cls=DjangoJSONEncoder))

def upload_parameter_file(ini_text, auth_user):
    '''
    upload legacy parameter file in ini format
    '''
    
    status = "success"
    message = ""

    
    return {"status" :  status, "message" : message}


