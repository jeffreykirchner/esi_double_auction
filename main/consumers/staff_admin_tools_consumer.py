'''
websocket session list
'''
import decimal
from asgiref.sync import sync_to_async
from decimal import Decimal

import json
import logging
import configparser
import main

from django.core.serializers.json import DjangoJSONEncoder

from main.consumers import SocketConsumerMixin
from main.consumers import create_new_session
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
    logger = logging.getLogger(__name__) 
    logger.info(f'upload_parameter_file text: {ini_text}')

    status = "success"
    message = ""

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

    #load values
    for parameter_set_period in parameter_set.parameter_set_periods.all():
        for i in range(parameter_set.number_of_buyers):
            value_list = config['buyer'+str(i+1)][str(parameter_set_period.period_number)].split(";")
            value_qs = main.models.ParameterSetPeriodSubjectValuecost.objects.filter(parameter_set_period_subject__id_number = i+1,
                                                                                     parameter_set_period_subject__subject_type = main.globals.SubjectType.BUYER,
                                                                                     parameter_set_period_subject__parameter_set_period = parameter_set_period)

            for j in range(4):
                if value_list[j] == "none":
                    value_qs[j].enabled = False
                else:
                    value_qs[j].value_cost = Decimal(value_list[j])

                value_qs[j].save()

    #load period settings
    for parameter_set_period in parameter_set.parameter_set_periods.all():
        parameter_set_period.y_scale_max = int(config['GameSettings']['maxPrice'])

        if config['priceCap'][str(parameter_set_period.period_number)] != "":
            parameter_set_period.price_cap = Decimal(config['priceCap'][str(parameter_set_period.period_number)])
            parameter_set_period.price_cap_enabled = True
            
        parameter_set_period.save()
    
    return {"status" :  status, "message" : message}


