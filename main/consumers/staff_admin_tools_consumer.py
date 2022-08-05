'''
websocket session list
'''
from asgiref.sync import sync_to_async
from decimal import Decimal

import json
import logging
import configparser
import main
import sys
import traceback

from django.core.serializers.json import DjangoJSONEncoder

from main.consumers import SocketConsumerMixin
from main.consumers import create_new_session
from main.consumers import take_submit_bid_offer
from main.consumers import take_next_period
from main.globals import todays_date


class StaffAdminToolsConsumer(SocketConsumerMixin):
    '''
    websocket admin tools
    '''    
    
    async def upload_parameters(self, event):
        '''
        upload legacy parameter file
        '''
        logger = logging.getLogger(__name__) 
        # logger.info(f"Upload Legacy parameter file {event}")

        self.user = self.scope["user"]
        logger.info(f"User {self.user}")

        message_text = event["message_text"]

        #build response
        message_data = {}
        message_data["result"] = await sync_to_async(take_upload_parameters)(message_text["ini_text"], self.user)

        message = {}
        message["messageType"] = event["type"]
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message,}, cls=DjangoJSONEncoder))
    
    async def upload_datafile(self, event):
        '''
        upload legacy datafile file
        '''
        logger = logging.getLogger(__name__) 
        # logger.info(f"Upload Legacy parameter file {event}")

        self.user = self.scope["user"]
        logger.info(f"User {self.user}")

        message_text = event["message_text"]

        #build response
        message_data = {}
        message_data["result"] = await sync_to_async(take_upload_datafile)(message_text["ini_text"], self.user)

        message = {}
        message["messageType"] = event["type"]
        message["messageData"] = message_data

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message,}, cls=DjangoJSONEncoder))

def take_upload_parameters(ini_text, auth_user):
    '''
    upload legacy parameter file in ini format
    '''
    logger = logging.getLogger(__name__) 
    logger.info(f'upload_parameter_file text: {ini_text}')

    status = "success"
    message = ""

    try:
        config = configparser.ConfigParser()
        config.read_string(ini_text)

        # logger.info(config['GameSettings']['gameName'])

        session = create_new_session(auth_user)
    
        session.title = "Parameter Upload " + todays_date().strftime("%m-%d-%Y")
        session.save()

        parameter_set = session.parameter_set
        parameter_set.number_of_buyers = int(config['GameSettings']['numberOfBuyers'])
        parameter_set.number_of_sellers = int(config['GameSettings']['numberOfSellers'])
        parameter_set.save()
        parameter_set.update_subject_counts()

        #add periods
        for i in range(1, int(config['GameSettings']['numberOfPeriods'])):
            parameter_set.add_session_period()

        #numboer of values and costs used
        value_count = [0,0,0,0,0,0,0,0,0,0,0]
        cost_count = [0,0,0,0,0,0,0,0,0,0,0]

        buyer_header = "buyer"
        seller_header = "seller"

        try:
            a = config[buyer_header+str(i+1)]
        except Exception as exc:
            buyer_header = "Buyer"
            seller_header = "Seller"

        #load values
        for parameter_set_period in parameter_set.parameter_set_periods.all():
            for i in range(parameter_set.number_of_buyers):
                value_list = config[buyer_header+str(i+1)][str(parameter_set_period.period_number)].split(";")
                value_qs = main.models.ParameterSetPeriodSubjectValuecost.objects.filter(parameter_set_period_subject__id_number = i+1,
                                                                                        parameter_set_period_subject__subject_type = main.globals.SubjectType.BUYER,
                                                                                        parameter_set_period_subject__parameter_set_period = parameter_set_period)

                value_qs = list(value_qs)

                for j in range(4):
                    if value_list[j] == "none" or value_list[j] == "":
                        value_qs[j].enabled = False
                    else:
                        value_qs[j].value_cost = Decimal(value_list[j])
                        value_count[parameter_set_period.period_number-1] += 1

                    value_qs[j].save()
        
        #load costs
        for parameter_set_period in parameter_set.parameter_set_periods.all():
            for i in range(parameter_set.number_of_buyers):
                cost_list = config[seller_header+str(i+1)][str(parameter_set_period.period_number)].split(";")
                cost_qs = main.models.ParameterSetPeriodSubjectValuecost.objects.filter(parameter_set_period_subject__id_number = i+1,
                                                                                        parameter_set_period_subject__subject_type = main.globals.SubjectType.SELLER,
                                                                                        parameter_set_period_subject__parameter_set_period = parameter_set_period)

                cost_qs = list(cost_qs)

                for j in range(4):
                    if cost_list[j] == "none" or cost_list[j] =="":
                        cost_qs[j].enabled = False
                    else:
                        cost_qs[j].value_cost = Decimal(cost_list[j])
                        cost_count[parameter_set_period.period_number-1] += 1

                    cost_qs[j].save()

        #load period settings
        for parameter_set_period in parameter_set.parameter_set_periods.all():
            parameter_set_period.y_scale_max = int(config['GameSettings']['maxPrice'])
            parameter_set_period.x_scale_max = max(value_count[parameter_set_period.period_number-1],
                                                cost_count[parameter_set_period.period_number-1])

            try:
                if config['priceCap'][str(parameter_set_period.period_number)] != "":
                    parameter_set_period.price_cap = Decimal(config['priceCap'][str(parameter_set_period.period_number)])
                    parameter_set_period.price_cap_enabled = True
            except Exception as exc:
                logger.warning(f"upload_parameter_file error: price cap not found")

            parameter_set_period.save()
        
        message = {"session" : session.id}
    except Exception as exc:
        message = sys.exc_info()
        message = ''.join(traceback.format_exception(*message))
        logger.warning(f"upload_parameter_file error: {message}")
        status="fail"
        session.parameter_set.delete()
    
    return {"status" :  status, "message" : message}

def take_upload_datafile(ini_text, auth_user):
    '''
    upload legacy parameter file in ini format
    '''
    logger = logging.getLogger(__name__) 
    # logger.info(f'take_upload_datafile text: {ini_text}')

    status = "success"
    message = ""

    result = take_upload_parameters(ini_text, auth_user)

    if result["status"] == "fail":
        return result
    else:
        #load parameters
        session = main.models.Session.objects.get(id=result["message"]["session"])

        session.title = "Datafile Upload " + todays_date().strftime("%m-%d-%Y")
        session.save()

        #load results
        config = configparser.ConfigParser()
        config.read_string(ini_text)

        session.start_experiment()

        try:
            for session_period in session.session_periods.all():
                period_number = str(session_period.period_number)
                config_period = config["Period" + period_number]
                bid_offer_count = int(config_period["BidAskCount"])

                for i in range(1, bid_offer_count+1):
                    bid_offer = config_period["BidAsk" +  str(i)].split(";")

                    bid_offer_id = "s" if bid_offer[2]=="ask" else "b"
                    bid_offer_id += str(bid_offer[1])

                    take_submit_bid_offer({"sessionID" : session.id,
                                        "bid_offer_id" : bid_offer_id,
                                        "bid_offer_amount" : bid_offer[4]})

                take_next_period({"sessionID" : session.id,})

                #price cap
                if config_period['PriceCap'] != "":
                    parameter_set_period = session_period.session.parameter_set.parameter_set_periods.get(period_number=period_number)
                    parameter_set_period.price_cap = Decimal(config_period['PriceCap'])
                    parameter_set_period.price_cap_enabled = True
                    parameter_set_period.save()
            
            session.finished=True
            session.save()
            message = {"session" : session.id}

        except Exception as exc:
            message = sys.exc_info()
            message = ''.join(traceback.format_exception(*message))
            logger.warning(f"upload_parameter_file error: {message}")
            status="fail"
            session.parameter_set.delete()

    return {"status" :  status, "message" : message}


