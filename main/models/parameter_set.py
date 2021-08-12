'''
sessions parameters
'''
import logging

from django.db import models
from django.db.utils import IntegrityError

from main.models import ConsentForms

import main

#experiment session parameters
class ParameterSet(models.Model):
    '''
    session parameters
    '''
    number_of_buyers = models.IntegerField(default=1, verbose_name="Number of buyers")       #number of buyers in the session
    number_of_sellers = models.IntegerField(default=1, verbose_name="Number of sellers")     #number of sellers in the session

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Study Parameter Set'
        verbose_name_plural = 'Study Parameter Sets'

    def from_dict(self, new_ps):
        '''
        load values from dict
        '''
        logger = logging.getLogger(__name__) 

        message = "Parameters loaded successfully."

        try:
            self.number_of_buyers = new_ps.get("number_of_buyers")
            self.number_of_sellers = new_ps.get("number_of_sellers")

            self.save()

            new_period_count = len(new_ps["periods"])
            current_period_count = self.parameter_set_periods.count()

            #update period count
            if new_period_count > current_period_count:
                for i in range(new_period_count-current_period_count):
                    self.add_session_period()
            elif current_period_count > new_period_count:
                for i in range(current_period_count-new_period_count):
                    self.remove_session_period()

            #copy periods
            for i in range(new_period_count):
                period = self.parameter_set_periods.get(period_number=i+1)
                period.from_dict(new_ps["periods"][i], True, True, True)

        except IntegrityError as exp:
            message = f"Failed to load parameter set: {exp}"
            logger.warning(message)

        return message

    def add_session_period(self):
        '''
        add new period to session
        '''

        last_period = self.parameter_set_periods.last()

        if last_period == None:
            period_number = 1
        else:
            period_number = last_period.period_number + 1

        parameter_set_period = main.models.ParameterSetPeriod()

        parameter_set_period.parameter_set = self
        parameter_set_period.period_number = period_number

        parameter_set_period.save()

        parameter_set_period.update_subject_count()

        return "success"
    
    def remove_session_period(self):
        '''
        remove last period froms session
        '''

        last_period = self.parameter_set_periods.last()

        if last_period == None:
            return "fail"
        
        if last_period.period_number <= 1:
            return "fail"
        
        last_period.delete()

        return "success"
    
    def update_subject_counts(self):
        '''
        update the number of subjects in the session
        '''

        status = "success"

        for i in self.parameter_set_periods.all():
            if i.update_subject_count() == "fail":
                status = "fail"

        return status
    
    def shift_values_or_costs(self, value_or_cost, period_number, direction):
        '''
        shift the values or costs for a period in the direction specified
        value_or_cost : string 'value' or 'cost'
        period : int 1 to N
        direction: string 'up' or 'down'
        '''

        parameter_set_period = self.parameter_set_periods.get(period_number = period_number)

        return parameter_set_period.shift_values_or_costs(value_or_cost, direction)
    
    def add_to_values_or_costs(self, value_or_cost, period_number, amount):
        '''
        add to all values or costs for a period by the amount specified
        value_or_cost : string 'value' or 'cost'
        period : int 1 to N
        amount: decimal
        '''

        parameter_set_period = self.parameter_set_periods.get(period_number = period_number)

        return parameter_set_period.add_to_values_or_costs(value_or_cost, amount)
    
    def copy_values_or_costs(self, value_or_cost, period_number):
        '''
        copy values or costs from previous period
        value_or_cost : string 'value' or 'cost'
        period : int 1 to N
        '''

        source_period = self.parameter_set_periods.get(period_number=period_number-1)
        target_period = self.parameter_set_periods.get(period_number=period_number)

        source_period_json = source_period.json()
        source_period_json["period_number"] = period_number

        if value_or_cost == "value":
            return target_period.from_dict(source_period_json, True, False, False)
        else:
            return target_period.from_dict(source_period_json, False, True, False)

    def get_number_of_periods(self):
        '''
        return the number of periods
        '''
        return self.parameter_set_periods.all().count()

    def get_buyer_list_json(self):
        '''
        return a json object of buyers
        '''

        buyer_list = []

        for i in range(1, self.number_of_buyers+1):
            buyer = {'id_number' : i,
                     'periods' : []}

            period_subject_list = main.models.ParameterSetPeriodSubject.objects.all() \
                                                                  .filter(id_number=i) \
                                                                  .filter(subject_type=main.globals.SubjectType.BUYER) \
                                                                  .filter(parameter_set_period__parameter_set=self) \
                                                                  .order_by('parameter_set_period__period_number')
            
            for period_subject in period_subject_list:
                period = {'id_number':period_subject.parameter_set_period.period_number,
                          'value_list':period_subject.get_value_cost_list()}
                
                buyer['periods'].append(period)

            buyer_list.append(buyer)

        return buyer_list

    def get_seller_list_json(self):
        '''
        return a json object of sellers
        '''

        seller_list = []

        for i in range(1, self.number_of_sellers+1):
            seller = {'id_number' : i,
                     'periods' : []}

            period_subject_list = main.models.ParameterSetPeriodSubject.objects.all() \
                                                                  .filter(id_number=i) \
                                                                  .filter(subject_type=main.globals.SubjectType.SELLER) \
                                                                  .filter(parameter_set_period__parameter_set=self) \
                                                                  .order_by('parameter_set_period__period_number')
            
            for period_subject in period_subject_list:
                period = {'id_number':period_subject.parameter_set_period.period_number,
                          'value_list':period_subject.get_value_cost_list()}
                
                seller['periods'].append(period)

            seller_list.append(seller)

        return seller_list

    def json(self):
        '''
        return json object of model
        '''
        return{

            "id" : self.id,
            "number_of_periods" : self.get_number_of_periods(),
            "number_of_buyers" : self.number_of_buyers,
            "number_of_sellers" : self.number_of_sellers,
            "periods" : [p.json()  for p in self.parameter_set_periods.all()],
        }
