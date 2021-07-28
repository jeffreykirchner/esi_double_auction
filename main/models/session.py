'''
session model
'''

import logging
import uuid

from asgiref.sync import sync_to_async
from django.conf import settings

from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_delete
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist

import main

from main.models import ParameterSet
from main.models import Parameters

#experiment sessoin
class Session(models.Model):
    '''
    session model
    '''
    parameter_set = models.ForeignKey(ParameterSet, on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length = 300, default="*** New Session ***")    #title of session
    start_date = models.DateField(default=now)                                   #date of session start

    channel_key = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name = 'Channel Key')     #unique channel to communicate on
    session_key = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name = 'Session Key')     #unique key for session to auto login subjects by id

    started =  models.BooleanField(default=False)                                #starts session and filll in session
    current_period = models.IntegerField(default=0)                              #current period of the session
    finished = models.BooleanField(default=False)                                #true after all session periods are complete

    invitations_sent = models.BooleanField(default=False)                        #true once invititations have been sent to subjects
    invitation_text =  models.CharField(max_length=10000, default="")            #text sent to subjects in experiment invititation
    invitation_text_subject = models.CharField(max_length=1000, default="")      #email subject text for experiment invititation

    soft_delete =  models.BooleanField(default=False)                            #hide session if true

    timestamp = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Experiment Session'
        verbose_name_plural = 'Experiment Sessions'
        ordering = ['-start_date']

    #get the current session day
    def get_current_session_period(self) :
        '''
        return session period given current period
        '''

        try:
            return self.session_periods.get(period_number = self.current_period)
        except ObjectDoesNotExist:
            return None

    def add_session_subjects(self):
        '''
        add subjects to session
        '''

        for sub in range(self.parameter_set.number_of_subjects):
            self.add_session_subject(sub+1)

    def add_session_subject(self, id_number):
        '''
        add single subject to session
        '''

        new_subject = main.models.SessionSubject()

        new_subject.session = self
        new_subject.id_number = id_number

        new_subject.save()

    def add_session_periods(self):
        '''
        create set of session periods
        '''
        #logger = logging.getLogger(__name__)

        for prd in range(self.parameter_set.number_of_periods):
            self.add_session_period(prd+1)

    def add_session_period(self, new_period):
        '''
        add new period to session
        '''
        logger = logging.getLogger(__name__)
        logger.info(f"add_session_period add period: {new_period} ")

        new_sd = main.models.SessionPeriod()

        new_sd.session = self
        new_sd.period_number = new_period
        new_sd.save()

    def get_start_date_string(self):
        '''
        get a formatted string of start date
        '''
        return  self.start_date.strftime("%#m/%#d/%Y")

    def send_invitations(self):
        '''
        send email invitations to subjects
        '''
        prm = Parameters.objects.first()
        text = self.invitation_text

        text = text.replace("[contact email]", prm.contactEmail)

        return main.globals.send_mass_invitations(self.session_subjects.filter(soft_delete=False), self.invitation_text_subject, text)

    def send_cancelation(self):
        '''
        send cancelation email to subjects
        '''
        prm = Parameters.objects.first()
        text = self.cancelation_text

        text = text.replace("[contact email]", prm.contactEmail)

        return main.globals.send_mass_invitations(self.session_subjects.filter(soft_delete=False), self.cancelation_text_subject, text)

    def complete(self):
        '''
        return true if session is complete
        '''

        return False

    def json(self):
        '''
        return json object of model
        '''
        return{
            "id":self.id,
            "title":self.title,
            "start_date":self.get_start_date_string(),
            "started":self.started,
            "current_period":self.current_period,
            "finished":self.finished,
            "parameter_set":self.parameter_set.json(),
            "session_periods":[i.json() for i in self.session_periods.all()]
        }


@receiver(post_delete, sender=Session)
def post_delete_parameterset(sender, instance, *args, **kwargs):
    '''
    use signal to delete associated parameter set
    '''
    if instance.parameter_set:
        instance.parameter_set.delete()
