'''
websocket session list
'''
from decimal import Decimal, DecimalException

import json
import logging

from asgiref.sync import sync_to_async

from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator

from main.models import ParameterSetPeriodSubjectValuecost
from main.models import ParameterSetPeriod

from main.models import SessionPeriodTradeBid
from main.models import SessionPeriodTradeOffer
from main.models import SessionPeriodTrade
from main.models.session_period_trade_offer import SessionPeriodTradeOffer

from main.consumers import SocketConsumerMixin
from main.consumers import get_session

from main.views import Session

from main.forms import SessionForm
from main.forms import PeriodForm
from main.forms import ValuecostForm

from main.globals import SubjectType
from main.globals import PriceCapType

from main.decorators import check_sesison_exists_ws
from main.decorators import check_user_is_owner_ws

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
        await self.send(text_data=json.dumps({'message': message,}, cls=DjangoJSONEncoder))
    
    async def update_session(self, event):
        '''
        update session parameters
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
        await self.send(text_data=json.dumps({'message': message}, cls=DjangoJSONEncoder))
    
    async def update_subject_count(self, event):
        '''
        add or remove a buyer or seller
        '''                
        #update subject count
        message_data = {}
        message_data["status"] = await sync_to_async(take_update_subject_count)(event["message_text"])
        message_data["session"] = await get_session(event["message_text"]["sessionID"])

        message = {}
        message["messageType"] = "update_session"
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}, cls=DjangoJSONEncoder))
    
    async def update_period_count(self, event):
        '''
        change the number of periods in a session
        '''
        #update subject count
        message_data = {}
        message_data["status"] = await sync_to_async(take_update_period_count)(event["message_text"])

        message_data["session"] = await get_session(event["message_text"]["sessionID"])

        message = {}
        message["messageType"] = "update_session"
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}, cls=DjangoJSONEncoder))
    
    async def update_valuecost(self, event):
        '''
        update a value or cost
        '''
        #update subject count
        message_data = {}
        message_data["status"] = await sync_to_async(take_update_valuecost)(event["message_text"])

        message_data["session"] = await get_session(event["message_text"]["sessionID"])

        message = {}
        message["messageType"] = "update_valuecost"
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}, cls=DjangoJSONEncoder))
    
    async def shift_value_or_cost(self, event):
        '''
        shift values or costs for current period up down between subjects
        '''
        #update subject count

        message_data = {}
        message_data["status"] = await sync_to_async(take_shift_value_or_cost)(event["message_text"])

        message_data["session"] = await get_session(event["message_text"]["sessionID"])

        message = {}
        message["messageType"] = "update_session"
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}, cls=DjangoJSONEncoder))
    
    async def copy_value_or_cost(self, event):
        '''
        copy values or costs form previous period
        '''
        #update subject count

        message_data = {}
        message_data["status"] = await sync_to_async(take_copy_value_or_cost)(event["message_text"])

        message_data["session"] = await get_session(event["message_text"]["sessionID"])

        message = {}
        message["messageType"] = "update_session"
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}, cls=DjangoJSONEncoder))

    async def update_period(self, event):
        '''
        update a period parameters
        '''
        #update subject count
        message_data = {}
        message_data["status"] = await sync_to_async(take_update_period)(event["message_text"])

        message_data["session"] = await get_session(event["message_text"]["sessionID"])

        message = {}
        message["messageType"] = "update_period"
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}, cls=DjangoJSONEncoder))
    
    async def import_parameters(self, event):
        '''
        import parameters from another session
        '''
        #update subject count
        message_data = {}
        message_data["status"] = await sync_to_async(take_import_parameters)(event["message_text"])

        message_data["session"] = await get_session(event["message_text"]["sessionID"])

        message = {}
        message["messageType"] = "import_parameters"
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}, cls=DjangoJSONEncoder))
    
    async def download_parameters(self, event):
        '''
        download parameters to a file
        '''
        #download parameters to a file
        message = {}
        message["messageType"] = "download_parameters"
        message["messageData"] = await take_download_parameters(event["message_text"])

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}, cls=DjangoJSONEncoder))

    async def start_experiment(self, event):
        '''
        start experiment
        '''
        #update subject count
        message_data = {}
        message_data["status"] = await take_start_experiment(event["message_text"])
        message_data["session"] = await get_session(event["message_text"]["sessionID"])

        message = {}
        message["messageType"] = event["type"]
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}, cls=DjangoJSONEncoder))
    
    async def reset_experiment(self, event):
        '''
        reset experiment, removes all trades, bids and asks
        '''
        #update subject count
        message_data = {}
        message_data["status"] = await take_reset_experiment(event["message_text"])
        message_data["session"] = await get_session(event["message_text"]["sessionID"])

        message = {}
        message["messageType"] = event["type"]
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}, cls=DjangoJSONEncoder))
    
    async def next_period(self, event):
        '''
        advance to next period in experiment
        '''
        #update subject count
        message_data = {}
        message_data["data"] = await sync_to_async(take_next_period)(event["message_text"])

        message = {}
        message["messageType"] = event["type"]
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}, cls=DjangoJSONEncoder))
    
    @check_user_is_owner_ws
    async def submit_bid_offer(self, event):
        '''
        take bid or offer
        '''

        # if not await sync_to_async(check_valid_user)(self.scope["user"], event["message_text"]["sessionID"]):
        #     return

        #update subject count
        message_data = {}
        message_data["result"] = await sync_to_async(take_submit_bid_offer)(event["message_text"])
        
        message = {}
        message["messageType"] = event["type"]
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}, cls=DjangoJSONEncoder))

    async def undo_bid_offer(self, event):
        '''
        undo last bid or offer
        '''

        #update subject count
        message_data = {}
        message_data["result"] = await take_undo_bid_offer(event["message_text"])
        
        message = {}
        message["messageType"] = event["type"]
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}, cls=DjangoJSONEncoder))

    async def add_to_all_values_or_costs(self, event):
        '''
        add to all values or costs by a specified amount
        '''
        
        #update subject count
        message_data = {}
        message_data["status"] = await sync_to_async(take_add_to_all_values_or_costs)(event["message_text"])

        message_data["session"] = await get_session(event["message_text"]["sessionID"])
        
        message = {}
        message["messageType"] = "update_session"
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}, cls=DjangoJSONEncoder))

def check_valid_user(user, session_id):
    '''
    check that user has access this session
    '''
    logger = logging.getLogger(__name__)
    if not user:
        logger.warning("check_valid_user: no auth user")
        return False
    
    try:        
        session = Session.objects.get(id=session_id)
    except ObjectDoesNotExist:
        logger.warning("check_valid_user: session does not exist")
        return False
    
    if user.is_superuser:
        return True

    if session.creator != user:
        logger.warning("check_valid_user: user is not creator of session")
        return False
    
    return True

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

def take_update_subject_count(data):
    '''
    take update to buyer or seller count for sessio
    param: data {"type":"buyer or seller","adjustment":"-1 or 1"} update to buyer or seller count
    '''
    logger = logging.getLogger(__name__) 
    logger.info(f"Update Buyer or Seller count: {data}")

    subject_type = data["type"]
    adjustment = data["adjustment"]
    session_id = data["sessionID"]

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
        logger.warning(f"take_update_valuecost session, not found ID: {id}")
    
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

def take_shift_value_or_cost(data):
    '''
    rotate values or costs up or down
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

def take_copy_value_or_cost(data):
    '''
    copy values or costs from previous periods
    '''   

    logger = logging.getLogger(__name__) 
    logger.info(f"Copy values or costs from previous period: {data}")

    status = "success"
    session_id = data["sessionID"]
    period = data["currentPeriod"]
    value_or_cost =  data["valueOrCost"]

    if period <= 1:
        return "fail"

    session = Session.objects.get(id=session_id)
    parameter_set = session.parameter_set

    message = parameter_set.copy_values_or_costs(value_or_cost, period)
    
    return status

def take_update_period(data):
    '''
    update period parameters
    '''   

    logger = logging.getLogger(__name__) 
    logger.info(f"Update period parameters: {data}")

    session_id = data["sessionID"]
    period_id = data["periodID"]

    form_data = data["formData"]

    try:        
        session_period = ParameterSetPeriod.objects.get(id=period_id)
    except ObjectDoesNotExist:
        logger.warning(f"take_update_period session period, not found ID: {period_id}")
    
    form_data_dict = {}

    for field in form_data:            
        form_data_dict[field["name"]] = field["value"]

    form = PeriodForm(form_data_dict, instance=session_period)

    if form.is_valid():
        #print("valid form")                
        form.save()              

        return {"value" : "success"}                      
                                
    logger.info("Invalid session form")
    return {"value" : "fail", "errors" : dict(form.errors.items())}

def take_import_parameters(data):
    '''
    import parameters from another session
    '''   
    logger = logging.getLogger(__name__) 
    logger.info(f"Import parameters: {data}")

    session_id = data["sessionID"]
    form_data = data["formData"]
    
    form_data_dict = {}

    for field in form_data:            
        form_data_dict[field["name"]] = field["value"]

    source_session = Session.objects.get(id=form_data_dict["session"])
    target_session = Session.objects.get(id=session_id)

    return target_session.parameter_set.from_dict(source_session.parameter_set.json())          

    # return {"value" : "fail" if "Failed" in message else "success",
    #         "message" : message}

@sync_to_async
def take_download_parameters(data):
    '''
    download parameters to a file
    '''   
    logger = logging.getLogger(__name__) 
    logger.info(f"Download parameters: {data}")

    session_id = data["sessionID"]

    session = Session.objects.get(id=session_id)
   
    return {"status" : "success", "parameter_set":session.parameter_set.json()}                      
                                
@sync_to_async
def take_start_experiment(data):
    '''
    start experiment
    '''   

    logger = logging.getLogger(__name__) 
    logger.info(f"Start Experiment: {data}")

    session_id = data["sessionID"]
    session = Session.objects.get(id=session_id)

    if not session.started:
        session.start_experiment()

    status = "success"
    
    return {"status" : status}

@sync_to_async
def take_reset_experiment(data):
    '''
    reset experiment remove bids and asks
    '''   

    logger = logging.getLogger(__name__) 
    logger.info(f"Reset Experiment: {data}")

    session_id = data["sessionID"]
    session = Session.objects.get(id=session_id)

    if session.started:
        session.started = False
        session.finished = False
        session.current_period = 1

        session.save()
        session.session_periods.all().delete()  
        session.session_subjects.all().delete() 

    status = "success"
    
    return {"status" : status}

def take_next_period(data):
    '''
    advance to next period in the experiment
    '''   

    logger = logging.getLogger(__name__) 
    logger.info(f"Advance to Next Period: {data}")

    session_id = data["sessionID"]
    session = Session.objects.get(id=session_id)

    if session.current_period == session.parameter_set.get_number_of_periods():
        session.finished = True
    else:
        session.current_period += 1

    session.save()

    status = "success"
    
    return {"status" : status,
            "current_period" : session.current_period,
            "finished" : session.finished}

def take_submit_bid_offer(data):
    '''
    take bid or offer
    data :{
        sessionID : int session pk,
        bid_offer_id : string example b1 or s2,
        bid_offer_amount : decimal 0.01 to 99.99
        }
    '''   

    logger = logging.getLogger(__name__) 
    logger.info(f"Take bid or offer: {data}")

    session_id = data["sessionID"]
    bid_offer_id = data["bid_offer_id"]
    bid_offer_amount = data["bid_offer_amount"]

    session = Session.objects.get(id=session_id)
    session_period = session.session_periods.get(period_number=session.current_period)
    session_period_trade = session_period.session_period_trades_a.get(trade_number=session_period.current_trade_number)
    # parameter_set_period = session.parameter_set.parameter_set_periods.get(period_number=session.current_period)

    status = "success"
    message = ""

    logger.info(f'take_submit_bid_offer: bid_offer_id {bid_offer_id}, bid_offer_amount {bid_offer_amount}')

    buyer_seller_id_1=None
    buyer_seller_id_2=None

    # get id
    try:
        buyer_seller_id_1 = bid_offer_id[0]
    except IndexError: 
        status = "fail"       
        message = "Error: Invalid ID, missing s or b."

    logger.info(f'take_submit_bid_offer: buyer_seller_id_1 {buyer_seller_id_1}')

    #check for s or b
    if status == "success": 
        if buyer_seller_id_1 != "s" and buyer_seller_id_1 != "S" and \
           buyer_seller_id_1 != "b" and buyer_seller_id_1 != "B":

            status = "fail"       
            message = "Error: Invalid ID, missing s or b."
    
    #check for id number
    if status == "success": 
        try:
            buyer_seller_id_2 = bid_offer_id[1:]
        except IndexError: 
            status = "fail"       
            message = f"Error: Invalid ID, incorrect number."
    
    #check that id number is a number
    if status == "success": 
        try:
            buyer_seller_id_2 = int(buyer_seller_id_2)
        except ValueError: 
            status = "fail"       
            message = f"Error: Invalid ID, incorrect number."

    logger.info(f'take_submit_bid_offer: buyer_seller_id_1 {buyer_seller_id_1}, buyer_seller_id_2 {buyer_seller_id_2}')

    #check amount is a decimal value
    if status == "success": 
        try:
            bid_offer_amount = Decimal(bid_offer_amount)
            bid_offer_amount = round(bid_offer_amount, 2)
        except DecimalException: 
            status = "fail"       
            message = f"Error: Invalid amount, not a decimal."
            logger.warning(f'take_submit_bid_offer: {message}')
    
    #check that bid / offer within valid range
    if status == "success":
        if bid_offer_amount <= 0 or bid_offer_amount > 99.999:
            status = "fail"       
            message = f"Error: 0 < Amount < 100 ."
            logger.warning(f'take_submit_bid_offer: {message}')
    
    #check bid / offer is under price cap, if applicable
    if status == "success":
        if session_period.get_price_cap_enabled():
            if session_period.get_price_cap_type() == PriceCapType.CEILING:
                if bid_offer_amount > session_period.get_price_cap():
                    status = "fail"       
                    message = f"Error: Amount exceeds price ceiling."
                    logger.warning(f'take_submit_bid_offer: {message}')
            else:
                if bid_offer_amount < session_period.get_price_cap():
                    status = "fail"       
                    message = f"Error: Amount below price floor."
                    logger.warning(f'take_submit_bid_offer: {message}')

    best_bid = session_period_trade.get_best_bid()
    best_offer = session_period_trade.get_best_offer()

    #check that type is a letter
    if status == "success":
        try:
            buyer_seller_id_1 = buyer_seller_id_1.lower()
        except TypeError: 
            status = "fail"       
            message = f"Error: Invalid ID, must be s or b."
            logger.warning(f'take_submit_bid_offer: {message}')

    #check for improvment
    if status == "success":
        if buyer_seller_id_1 == "s":
            if best_offer and bid_offer_amount >= best_offer.amount:
                message = f"Error: Offer must be lower than ${best_offer.amount}."
                logger.warning(f'take_submit_bid_offer: {message}')
                status = "fail"
        else:
             if best_bid and bid_offer_amount <= best_bid.amount:
                message = f"Error: Bid must be greater than ${best_bid.amount}."
                logger.warning(f'take_submit_bid_offer: {message}')
                status = "fail"
    
    #check for valid buyer or seller ID
    if status == "success":
        if buyer_seller_id_1 == "s":
            if buyer_seller_id_2 > session.parameter_set.number_of_sellers:
                message = f"Error: Seller {buyer_seller_id_2} does not exist."
                logger.warning(f'take_submit_bid_offer: {message}')
                status = "fail"
        else:
            if buyer_seller_id_2 > session.parameter_set.number_of_buyers:
                message = f"Error: Buyer {buyer_seller_id_2} does not exist."
                logger.warning(f'take_submit_bid_offer: {message}')
                status = "fail"
    
    #check that units remain for trading
    if status == "success":
        label = ""
        if buyer_seller_id_1 == "s":
            session_subject_period = session.session_subjects \
                                            .get(id_number=buyer_seller_id_2, subject_type=SubjectType.SELLER) \
                                            .get_session_subject_period(session_period)
            label = "Seller"
        else:
            session_subject_period = session.session_subjects \
                                            .get(id_number=buyer_seller_id_2, subject_type=SubjectType.BUYER) \
                                            .get_session_subject_period(session_period)
            label = "Buyer"
        
        if not session_subject_period.get_current_value_cost():
            message = f"Error: {label} {session_subject_period.session_subject.id_number} has no units available."
            logger.warning(f'take_submit_bid_offer: {message}')
            status = "fail"

    if status == "success": 
        if buyer_seller_id_1 == "s":
            # create offer           
            offer = SessionPeriodTradeOffer()

            offer.session_period_trade = session_period_trade
            offer.cost = session_subject_period.get_current_value_cost()
            offer.session_subject_period = session_subject_period

            # logger.info(f'best bid: {best_bid.amount} offer : {bid_offer_amount}')

            if best_bid and best_bid.amount >= bid_offer_amount:
                bid_offer_amount = best_bid.amount

                #record trade
                session_period_trade.buyer = best_bid.session_subject_period
                session_period_trade.buyer_value = best_bid.session_subject_period.get_current_value_cost()

                session_period_trade.seller = session_subject_period
                session_period_trade.seller_cost = session_subject_period.get_current_value_cost()

                session_period_trade.trade_complete = True
                session_period_trade.trade_price = bid_offer_amount

                session_period_trade.save()

                #advance buyer and seller to next unit in schedule
                best_bid.session_subject_period.current_unit_number += 1
                best_bid.session_subject_period.save()

                session_subject_period.current_unit_number += 1
                session_subject_period.save()

                #create new trade
                session_period.current_trade_number += 1
                session_period.save()

                new_session_period_trade = SessionPeriodTrade()
                new_session_period_trade.session_period = session_period
                new_session_period_trade.trade_number = session_period.current_trade_number
                new_session_period_trade.save()
                
                message = f'Buyer {best_bid.session_subject_period.session_subject.id_number} \
                            trades with Seller {session_subject_period.session_subject.id_number} for ${bid_offer_amount:0.2f}.'

                realized_gains_from_trade = session_period.get_total_gains_from_trade()
                efficiency = session_period.get_period_efficiency()
            else:    
                message = f'Seller {buyer_seller_id_2} offers to sell for ${bid_offer_amount:0.2f}.'
                realized_gains_from_trade = -1
                efficiency = -1

            offer.amount = bid_offer_amount
            offer.save()

            return {"status" : status,
                    "message" : message,
                    "realized_gains_from_trade" : realized_gains_from_trade,
                    "efficiency" : efficiency,
                    "current_best_bid" : i.get_bid_offer_string() if (i:=session_period.get_current_best_bid()) else "---",
                    "current_best_offer" : i.get_bid_offer_string() if (i:=session_period.get_current_best_offer()) else "---",
                    "trade_list" : session_period.get_trade_list_json(),
                    "offer_list" : session_period.get_offer_list_json()}
        else:
            #create bid
            bid = SessionPeriodTradeBid()

            bid.session_period_trade = session_period_trade
            bid.value = session_subject_period.get_current_value_cost()
            bid.session_subject_period = session_subject_period

            if best_offer and best_offer.amount <= bid_offer_amount:
                bid_offer_amount = best_offer.amount

                #record trade
                session_period_trade.buyer = session_subject_period 
                session_period_trade.buyer_value = session_subject_period.get_current_value_cost()

                session_period_trade.seller = best_offer.session_subject_period
                session_period_trade.seller_cost = best_offer.session_subject_period.get_current_value_cost()

                session_period_trade.trade_complete = True
                session_period_trade.trade_price = bid_offer_amount

                session_period_trade.save()

                #advance buyer and seller to next unit in schedule
                best_offer.session_subject_period.current_unit_number += 1
                best_offer.session_subject_period.save()

                session_subject_period.current_unit_number += 1
                session_subject_period.save()

                #create new trade
                session_period.current_trade_number += 1
                session_period.save()

                new_session_period_trade = SessionPeriodTrade()
                new_session_period_trade.session_period = session_period
                new_session_period_trade.trade_number = session_period.current_trade_number
                new_session_period_trade.save()

                message = f'Buyer {session_subject_period.session_subject.id_number} \
                            trades with Seller {best_offer.session_subject_period.session_subject.id_number} for ${bid_offer_amount:0.2f}.'

                realized_gains_from_trade = session_period.get_total_gains_from_trade()
                efficiency = session_period.get_period_efficiency()
            else:
                message = f'Buyer {buyer_seller_id_2} bids to buy for ${bid_offer_amount:0.2f}.'
                realized_gains_from_trade = -1
                efficiency = -1

            bid.amount = bid_offer_amount
            bid.save()

            return {"status" : status,
                    "message" : message,
                    "realized_gains_from_trade" : realized_gains_from_trade,
                    "efficiency" : efficiency,
                    "current_best_offer" : i.get_bid_offer_string() if (i:=session_period.get_current_best_offer()) else "---",
                    "current_best_bid" : i.get_bid_offer_string() if (i:=session_period.get_current_best_bid()) else "---",
                    "trade_list" : session_period.get_trade_list_json(),            
                    "bid_list" : session_period.get_bid_list_json()}

    return {"status" : "fail", "message" : message}

@sync_to_async
def take_undo_bid_offer(data):
    '''
    take undo bid or offer
    '''   

    logger = logging.getLogger(__name__) 
    logger.info(f"Take undo bid or offer: {data}")

    session_id = data["sessionID"]

    session = Session.objects.get(id=session_id)
    session_period = session.session_periods.get(period_number=session.current_period)
    session_period_trade = session_period.session_period_trades_a.get(trade_number=session_period.current_trade_number)

    best_bid = session_period_trade.get_best_bid()
    best_offer = session_period_trade.get_best_offer()

    message = "Nothing to undo."

    if not best_bid and not best_offer and session_period_trade.trade_number > 1:
        # no bids for offers for this trade and this is not first trade

        #remove current trade
        session_period.current_trade_number -= 1
        session_period.save()

        session_period_trade.delete()

        #open previous trade and its best bid and offer
        session_period_trade = session_period.session_period_trades_a.get(trade_number=session_period.current_trade_number)
        session_period_trade.trade_complete = False
        session_period_trade.save()

        session_period_trade.buyer.current_unit_number -= 1
        session_period_trade.buyer.save()

        session_period_trade.seller.current_unit_number -= 1
        session_period_trade.seller.save()

        best_bid = session_period_trade.get_best_bid()
        best_offer = session_period_trade.get_best_offer()

    if best_bid or best_offer:
        if best_bid and not best_offer:
            #no offers, remove best bid
            message = f"Buyer {best_bid.session_subject_period.session_subject.id_number}'s bid removed."
            best_bid.delete()
        elif best_offer and not best_bid:
            #no bids, remove best offer
            message = f"Seller {best_offer.session_subject_period.session_subject.id_number}'s offer removed."
            best_offer.delete()
        elif best_bid.timestamp > best_offer.timestamp:
            #bid is newer, remove it
            message = f"Buyer {best_bid.session_subject_period.session_subject.id_number}'s bid removed."
            best_bid.delete()
        else:
            #offer is newer, remove it
            message = f"Seller {best_offer.session_subject_period.session_subject.id_number}'s offer removed."
            best_offer.delete()

    return {"current_best_offer" : i.get_bid_offer_string() if (i:=session_period.get_current_best_offer()) else "---",
            "current_best_bid" : i.get_bid_offer_string() if (i:=session_period.get_current_best_bid()) else "---",
            "trade_list" : session_period.get_trade_list_json(),  
            "message" : message,          
            "bid_list" : session_period.get_bid_list_json(),
            "offer_list" : session_period.get_offer_list_json(),}

def take_add_to_all_values_or_costs(data):
    '''
    take add to all values or costs
    '''   

    logger = logging.getLogger(__name__) 
    logger.info(f"Take add to all values or costs: {data}")

    session_id = data["sessionID"]
    period = data["currentPeriod"]
    values_or_costs = data["valueOrCost"]
    amount = data["amount"]

    session = Session.objects.get(id=session_id)
    parameter_set = session.parameter_set

    #check amount is a valid deciamal amount
    try:
        amount = Decimal(amount)
    except DecimalException: 
              
        message = f"Error: Invalid amount, not a decimal."
        logger.warning(f'take_submit_bid_offer: {message}')

        return "fail"

    status = parameter_set.add_to_values_or_costs(values_or_costs, period, amount)

    return status