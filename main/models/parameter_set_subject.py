'''
sessions parameters
'''
from django.db import models
from django.db.utils import IntegrityError

from main.models import ParameterSet

import main

#experiment session parameters
class ParameterSetSubject(models.Model):
    '''
    session parameters
    '''

    parameter_set = models.ForeignKey(ParameterSet,on_delete=models.CASCADE, related_name="parameter_set_subjects")

    id_number = models.IntegerField(null=True, verbose_name = 'ID Number in Session')                                   #local id number in session

    timestamp = models.DateTimeField(auto_now_add = True)
    updated= models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Study Parameter Set Subject'
        verbose_name_plural = 'Study Parameter Sets Subjets'

    def setup_from_dict(self, new_ps):
        '''
        load values from dict
        '''

        message = "Parameters loaded successfully."

        try:
            self.parameter_set = main.models.ParameterSet.objects.get(id=new_ps.get("parameter_set"))
            self.id_number = new_ps.get("id_number")

            self.save()

        except IntegrityError as exp:
            message = f"Failed to load parameter set subject: {exp}"
            #logger.info(message)

        return message

    def setup(self,new_ps):
        '''
        copy another parameter set into this one
        '''

        self.save()

        self.parameter_set = new_ps.parameter_set
        self.id_number = new_ps.id_number

        self.save()

    def json(self):
        '''
        return json object of model
        '''
        return{

            "id" : self.id,
            "consent_form_required" : self.id_number,
        }
