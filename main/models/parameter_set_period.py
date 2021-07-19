'''
session's period parameters
'''
from decimal import Decimal

from django.db import models
from django.db.utils import IntegrityError

from main.models import ParameterSet

import main

#experiment session parameters
class ParameterSetPeriod(models.Model):
    '''
    session single period parameters 
    '''

    parameter_set = models.ForeignKey(ParameterSet, on_delete=models.CASCADE,  related_name="parameter_set_periods")

    period_number = models.IntegerField(verbose_name='Period number')                                       #period from 1 - N in parameter set
    price_cap = models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name = 'Price Cap')  #max bid or offer allowed in this period 
    price_cap_enabled = models.BooleanField(default=False, verbose_name = 'Price Cap Enabled')              #if true, enforce price cap

    y_scale_max = models.IntegerField(verbose_name='Y Scale Max', default=10)                               #max Y scale of period 
    x_scale_max = models.IntegerField(verbose_name='X Scale Max', default=10)                               #max X scale of period 

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Period Parameter Set'
        verbose_name_plural = 'Period Parameter Sets'
        ordering = ['period_number']
        constraints = [
            models.UniqueConstraint(fields=['parameter_set', 'period_number'], name='unique_period'),
        ]

    def update_subject_count(self):
        '''
        create new parameter set subject set

        subject_type: SubjectType , BUYER or SELLER
        period_number: Int 1 to N
        id_number: Int unique ID within buyer or seller group, 1 to N
        '''

        #remove extra buyers
        buyers_excess = self.parameter_set_period_subjects.filter(subject_type=main.globals.SubjectType.BUYER,
                                                                  id_number__gt = self.parameter_set.number_of_buyers)

        if buyers_excess != None:
            buyers_excess.delete()


        #remove extra sellers
        sellers_excess = self.parameter_set_period_subjects.filter(subject_type=main.globals.SubjectType.SELLER,
                                                                  id_number__gt = self.parameter_set.number_of_sellers)

        if sellers_excess != None:
            sellers_excess.delete()

        #add needed buyers
        current_buyer_count = self.parameter_set_period_subjects.filter(subject_type=main.globals.SubjectType.BUYER)

        for i in range(current_buyer_count.count() + 1, self.parameter_set.number_of_buyers+1):
            subject = main.models.ParameterSetPeriodSubject()

            subject.parameter_set_period = self
            subject.subject_type = main.globals.SubjectType.BUYER
            subject.id_number = i

            subject.save()

            for i in range(4):
                ps_value_cost = main.models.ParameterSetPeriodSubjectValuecost()

                ps_value_cost.parameter_set_period_subject = subject
                ps_value_cost.value_cost = 0

                ps_value_cost.save()
        
        #add needed sellers
        current_seller_count = self.parameter_set_period_subjects.filter(subject_type=main.globals.SubjectType.SELLER)

        for i in range(current_seller_count.count() + 1, self.parameter_set.number_of_sellers+1):
            subject = main.models.ParameterSetPeriodSubject()

            subject.parameter_set_period = self
            subject.subject_type = main.globals.SubjectType.SELLER
            subject.id_number = i

            subject.save()

            for i in range(4):
                ps_value_cost = main.models.ParameterSetPeriodSubjectValuecost()

                ps_value_cost.parameter_set_period_subject = subject
                ps_value_cost.value_cost = 0

                ps_value_cost.save()

        return "success"

    def remove_parameter_set_subject(self, subject_type):
        '''
        remove the last parameter set subject

        create new parameter set subject
        parameter_set: ParameterSet to attach subject to
        subject_type: SubjectType , BUYER or SELLER
        period_number: Int 1 to N
        id_number: Int unique ID within buyer or seller group, 1 to N
        '''

        last_subject = self.parameter_set_period_subjects.filter(subject_type=subject_type).last()

        if last_subject == None:
            return "fail"

        self.parameter_set_period_subjects.filter(subject_type=subject_type, id_number=last_subject.id_number).delete()

        return "success"
    
    def get_buyer_list(self):
        '''
        return a list of all the buyers in the this period
        '''

        return [b for b in self.parameter_set_period_subjects.all() if b.subject_type == 'Buyer']

    def get_seller_list(self):
        '''
        return a list of all the buyers in the this period
        '''

        return [s for s in self.parameter_set_period_subjects.all() if s.subject_type == 'Seller']
    
    def shift_values_or_costs(self, value_or_cost, direction):
        '''
        shift values or costs in the direction specficied
        value_or_cost : string 'value' or 'cost'
        direction: string 'up' or 'down'
        '''


        if value_or_cost == 'value':
            user_list = self.get_buyer_list()
        else:
            user_list = self.get_seller_list()

        if len(user_list) <= 1:
            return "fail"

        for i in range(len(user_list)):
                user_list[i].id_number = 10000 + i
                user_list[i].save()

        if direction == "up":
            
            for i in range(1, len(user_list)):
                user_list[i].id_number = i
                user_list[i].save()
            
            user_list[0].id_number = len(user_list)
            user_list[0].save()
        else:
            for i in range(len(user_list)-1):
                user_list[i].id_number = i + 2
                user_list[i].save()
            
            user_list[len(user_list)-1].id_number = 1
            user_list[len(user_list)-1].save()

        return "success"

    def from_dict(self, source, copy_buyers, copy_sellers, copy_price_cap):
        '''
        copy source values into this period
        source : dict object of period
        '''
        
        message = "Parameters loaded successfully."

        self.period_number = source.get("period_number")
        self.y_scale_max = source.get("y_scale_max")
        self.x_scale_max = source.get("x_scale_max")

        if copy_price_cap:
            self.price_cap = Decimal(source.get("price_cap"))
            self.price_cap_enabled = True if source.get("price_cap_enabled") == "True" else False

        #self.parameter_set = ParameterSet.objects.get(id=source.get("parameter_set"))

        self.update_subject_count()

        self.save()

        if copy_buyers:
            buyer_list = self.get_buyer_list()

            for i in range(len(buyer_list)):
                buyer_list[i].from_dict(source.get("buyers")[i])
        
        if copy_sellers:
            seller_list = self.get_seller_list()

            for i in range(len(seller_list)):
                seller_list[i].from_dict(source.get("sellers")[i])

        return message

    def get_demand(self):
        '''
        return a list reprsenting the demand for this period
        '''

        buyer_list = self.get_buyer_list()

        value_qs = main.models.ParameterSetPeriodSubjectValuecost.objects.filter(parameter_set_period_subject__in = buyer_list) \
                                                                         .filter(enabled = True) \
                                                                         .order_by('-value_cost')

        return [i.json() for i in value_qs]
    
    def get_supply(self):
        '''
        return a list reprsenting the supply for this period
        '''

        buyer_list = self.get_seller_list()

        cost_qs = main.models.ParameterSetPeriodSubjectValuecost.objects.filter(parameter_set_period_subject__in = buyer_list) \
                                                                        .filter(enabled = True) \
                                                                        .order_by('value_cost')

        return [i.json() for i in cost_qs]

    def json(self):
        '''
        return json object of model
        '''

        supply = self.get_supply()
        demand = self.get_demand()

        eq_price = 0
        eq_quantity = None

        for i in range(len(supply)):

            if len(demand) < i+1:
                break

            if float(supply[i]['value_cost']) >= float(demand[i]['value_cost']):
                eq_quantity = i                
                break   
        
        if eq_quantity and eq_quantity > 0:
            eq_price = (float(supply[eq_quantity-1]['value_cost']) + float(demand[eq_quantity-1]['value_cost'])) / 2
            eq_price = round(eq_price, 3)

        return{

            "id" : self.id,
            #"parameter_set" : self.parameter_set.id,
            "period_number" : self.period_number,
            "y_scale_max" : self.y_scale_max,
            "x_scale_max" : self.x_scale_max,
            "price_cap" : str(self.price_cap),
            "price_cap_enabled" : "True" if self.price_cap_enabled else "False",
            "buyers" : [b.json() for b in self.get_buyer_list()],
            "sellers" : [s.json() for s in self.get_seller_list()],
            "demand" : demand,
            "supply" : supply,
            "eq_price" : eq_price,
            "eq_quantity" : eq_quantity,
        }
