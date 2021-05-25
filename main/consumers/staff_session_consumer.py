'''
websocket session list
'''
import json
import logging
from main.forms.valuecost_form import ValuecostForm
from main.models.parameter_set_period_subject_valuecost import ParameterSetPeriodSubjectValuecost

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
    
    async def update_subject_count(self, event):
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
    
    async def update_period_count(self, event):
        '''
        change the number of periods in a session
        '''

        
        
        #update subject count
        message_data = {}
        message_data["status"] = await take_update_period_count(event["message_text"])

        message_data["session"] = await get_session(event["message_text"]["sessionID"])

        message = {}
        message["messageType"] = "update_session"
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
    
    async def update_valuecost(self, event):
        '''
        update a value or cost
        '''
        #update subject count
        message_data = {}
        message_data["status"] = await take_update_valuecost(event["message_text"])

        message_data["session"] = await get_session(event["message_text"]["sessionID"])

        message = {}
        message["messageType"] = "update_valuecost"
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
    
    async def shift_value_or_cost(self, event):
        '''
        shift values or costs for current period up down between subjects
        '''
        #update subject count

        message_data = {}
        message_data["status"] = await take_shift_value_or_cost(event["message_text"])

        message_data["session"] = await get_session(event["message_text"]["sessionID"])

        message = {}
        message["messageType"] = "update_session"
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
    
    async def copy_value_or_cost(self, event):
        '''
        copy values or costs form previous period
        '''
        #update subject count

        message_data = {}
        message_data["status"] = await take_copy_value_or_cost(event["message_text"])

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
    period_number = data["current_period"]

    session = Session.objects.get(id=session_id)

    parameter_set = session.parameter_set

    if parameter_set == None:
        return "fail"

    if subject_type == "SELLER":
        if adjustment == 1:
           parameter_set.number_of_sellers += 1
        elif parameter_set.number_of_sellers > 1 :
            parameter_set.number_of_sellers -= 1
        else:
            return "fail"
    else:
        if adjustment == 1:
           parameter_set.number_of_buyers += 1
        elif parameter_set.number_of_buyers > 1 :
            parameter_set.number_of_buyers -= 1
        else:
            return "fail"    

    parameter_set.save()
    
    return parameter_set.update_subject_counts()

@sync_to_async
def take_update_period_count(data):
    '''
    update the number of periods
    '''   

    logger = logging.getLogger(__name__) 
    logger.info(f"Update period count: {data}")

    adjustment = data["adjustment"]
    session_id = data["sessionID"]

    session = Session.objects.get(id=session_id)

    parameter_set = session.parameter_set

    if adjustment == 1:
        return parameter_set.add_session_period()
    else:
        return parameter_set.remove_session_period()

@sync_to_async
def take_update_valuecost(data):
    '''
    update a value or cost for session
    '''   

    logger = logging.getLogger(__name__) 
    logger.info(f"Update value or cost: {data}")

    session_id = data["sessionID"]
    id = data["id"]

    form_data = data["formData"]

    try:        
        valuecost = ParameterSetPeriodSubjectValuecost.objects.get(id=id)
    except ObjectDoesNotExist:
        logger.warning(f"take_update_session_form session, not found: {session_id}")
    
    form_data_dict = {}

    for field in form_data:            
        form_data_dict[field["name"]] = field["value"]

    form = ValuecostForm(form_data_dict, instance=valuecost)

    if form.is_valid():
        #print("valid form")                
        form.save()              

        return {"value" : "success"}                      
                                
    logger.info("Invalid session form")
    return {"value" : "fail", "errors" : dict(form.errors.items())}

@sync_to_async
def take_shift_value_or_cost(data):
    '''
    shift values or costs up or down
    '''   

    logger = logging.getLogger(__name__) 
    logger.info(f"shift values up or down: {data}")

    status = "success"
    session_id = data["sessionID"]
    period = data["currentPeriod"]
    value_or_cost =  data["valueOrCost"]
    direction =  data["direction"]

    session = Session.objects.get(id=session_id)
    parameter_set = session.parameter_set

    status = parameter_set.shift_values_or_costs(value_or_cost, period, direction)
    
    return status

@sync_to_async
def take_copy_value_or_cost(data):
    '''
    copy values or costs from previous periods
    '''   

    logger = logging.getLogger(__name__) 
    logger.info(f"shift values up or down: {data}")

    status = "success"
    session_id = data["sessionID"]
    period = data["currentPeriod"]
    value_or_cost =  data["valueOrCost"]

    if period <= 1:
        return "fail"

    session = Session.objects.get(id=session_id)
    parameter_set = session.parameter_set

    status = parameter_set.copy_values_or_costs(value_or_cost, period)
    
    return "success"

