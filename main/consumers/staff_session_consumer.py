'''
websocket session list
'''
import json
import logging

from asgiref.sync import sync_to_async

from django.core.exceptions import ObjectDoesNotExist

from main.consumers import SocketConsumerMixin
from main.consumers import get_session

from main.views import Session

from main.forms import SessionForm
from main.globals import SubjectType

class StaffSessionConsumer(SocketConsumerMixin):
    '''
    websocket session list
    '''    

    async def get_session(self, event):
        '''
        return a list of sessions
        '''
        logger = logging.getLogger(__name__) 
        logger.info(f"Get Session {event}")

        #build response
        message_data = {}
        message_data["session"] = await get_session(event["message_text"]["sessionID"])

        message = {}
        message["messageType"] = event["type"]
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
    
    async def update_session(self, event):
        '''
        return a list of sessions
        '''
        logger = logging.getLogger(__name__) 
        logger.info(f"Update Session: {event}")

        #build response
        message_data = {}
        message_data = await take_update_session_form(event["message_text"])

        message = {}
        message["messageType"] = event["type"]
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
    
    async def update_subject_count(self,event):
        '''
        add or remove a buyer or seller
        '''

        logger = logging.getLogger(__name__) 
        logger.info(f"Update Buyer or Seller count: {event}")

        
        #update subject count
        message_data = {}
        message_data["status"] = await take_update_subject_count(event["message_text"])

        message_data["session"] = await get_session(event["message_text"]["sessionID"])

        message = {}
        message["messageType"] = "update_session"
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))



#local sync_to_asyncs
@sync_to_async
def take_update_session_form(data):
    '''
    take session form data and update session or return errors
    param: data {json} incoming form and session data
    '''

    logger = logging.getLogger(__name__)
    logger.info(f'take_update_session_form: {data}')

    session_id = data["sessionID"]
    form_data = data["formData"]

    try:        
        session = Session.objects.get(id=session_id)
    except ObjectDoesNotExist:
        logger.warning(f"take_update_session_form session, not found: {session_id}")
    
    form_data_dict = {}

    for field in form_data:            
        form_data_dict[field["name"]] = field["value"]

    form = SessionForm(form_data_dict, instance=session)

    if form.is_valid():
        #print("valid form")                
        form.save()              

        return {"status":"success", "session" : session.json()}                      
                                
    logger.info("Invalid session form")
    return {"status":"fail", "errors":dict(form.errors.items())}

@sync_to_async
def take_update_subject_count(data):
    '''
    take update to buyer or seller count for sessio
    param: data {"type":"buyer or seller","adjustment":"-1 or 1"} update to buyer or seller count
    '''

    subject_type = data["type"]
    adjustment = data["adjustment"]
    session_id = data["sessionID"]

    session = Session.objects.get(id=session_id)

    if subject_type == "SELLER":
        subject_type = SubjectType.SELLER
    else:
        subject_type = SubjectType.BUYER

    if adjustment == 1:
        session.parameter_set.add_parameter_set_subject(subject_type)
    else:
        session.parameter_set.remove_parameter_set_subject(subject_type)

    return "success"

    

