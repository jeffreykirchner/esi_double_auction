'''
session subject model
'''
import uuid

from django.db import models

from main.models import Session

#subject in session
class SessionSubject(models.Model):
    '''
    session subject model
    '''
    session = models.ForeignKey(Session,on_delete=models.CASCADE, related_name="session_subjects")

    id_number = models.IntegerField(null=True, verbose_name = 'ID Number in Session')                                   #local id number in session

    login_key = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name = 'Login Key')                        #log in key used to ID subject for URL login
    name = models.CharField(max_length = 300,default = 'Subject Name', verbose_name = 'Subject Name')                   #subject name
    contact_email = models.CharField(max_length = 300, default = 'panther@chapman.edu',verbose_name = 'Subject Email')  #contact email address
    student_id = models.CharField(max_length = 300, default = '123456789', verbose_name = 'Student ID Number')          #student ID number

    consent_required = models.BooleanField(default=True,verbose_name = 'Consent Form Signed')          #true if subject has done consent form
    consent_signature = models.CharField(max_length = 300,default = '', verbose_name = 'Consent Form Signature')

    display_color = models.CharField(max_length = 300,default = '#000000',verbose_name = 'Graph Color')

    soft_delete =  models.BooleanField(default=False)                                                 #hide subject if true

    timestamp = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id_number', 'session'], name='Session_subject')
        ]
        verbose_name = 'Session Subject'
        verbose_name_plural = 'Session Subjects'

    #return json object of class
    def json(self):
        '''
        json object of model
        '''

        return {
            "id" : self.id,
            "name" : self.name,
            "contact_email" : self.contact_email,
            "student_id" : self.student_id,
            "consent_required" : self.consent_required,
            "questionnaire1_required" : self.questionnaire1_required,
            "questionnaire2_required" : self.questionnaire2_required,
        }
