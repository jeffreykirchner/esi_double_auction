'''
build tz aware date for today
'''
#import logging

from datetime import datetime
import pytz
from main.models import Parameters

def todays_date():
    '''
        Get today's server time zone adjusted date time object with zeroed time
    '''
    #logger = logging.getLogger(__name__)

    prm = Parameters.objects.first()
    tmz = pytz.timezone(prm.experiment_time_zone)

    d_today = datetime.now(tmz)
    d_today = d_today.replace(hour=0,minute=0, second=0,microsecond=0)       
    
    return d_today