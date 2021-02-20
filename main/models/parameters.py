'''
site parameters
'''

from django.db import models

#gloabal parameters for site
class Parameters(models.Model):
    '''
    site parameters
    '''
    contactEmail =  models.CharField(max_length = 1000,default = "JohnSmith@abc.edu")      #primary contact for subjects
    experimentTimeZone = models.CharField(max_length = 1000,default = "US/Pacific")        #time zone the experiment is in

    siteURL = models.CharField(max_length = 200,default = "https://www.google.com/")       #site URL used for display in emails
    test_email_account = models.CharField(max_length = 1000,default = "")                  #email account used for debug mode emails

    invitation_text_subject = models.CharField(max_length = 1000,default = "")             #email subject text for the single day invitation
    invitation_text = models.CharField(max_length = 10000,default = "")                    #email text for the single day invitation

    cancelation_text_subject = models.CharField(max_length = 1000,default = "")            #email subject text when an experiment is canceled
    cancelation_text = models.CharField(max_length = 10000,default = "")                   #email text when an experiment is canceled

    questionnaire1Required = models.BooleanField(default=True)                             #enable pre experiment questionnaire
    questionnaire2Required = models.BooleanField(default=True)                             #enable post experiment questionnaire

    staffsessionHelpText = models.CharField(max_length = 5000,default = "")                # help text shown to staff
    staffHomeHelpText = models.CharField(max_length = 5000,default = "")                   # help text shown to staff home page

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return "Site Parameters"

    class Meta:
        verbose_name = 'Parameters'
        verbose_name_plural = 'Parameters'

    def json(self):
        '''
        model json object
        '''
        return{
            "id" : self.id
        }
        