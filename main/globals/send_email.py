
'''
global email functions
'''
from smtplib import SMTPException

import logging

from django.conf import settings
from django.core.mail import send_mass_mail

from main.models import Parameters

def send_mass_invitations(user_list, message_subject, message):
    '''
    send mass email
    user_list: list of users to send email to
    message_subject: the subject of the email
    message: body of the email
    '''
    logger = logging.getLogger(__name__)
    logger.info("Send mass email to list")

    prm = Parameters.objects.first()

    message_list = []
    message_list.append(())
    from_email = get_from_email()

    block_count = 0
    cnt = 0
    for usr in user_list:

        if cnt == 100:
            cnt = 0
            block_count += 1
            message_list.append(())

        #fill in parameters
        new_message = message.replace("[subject name]", usr.name)
        new_message = new_message.replace("[log in link]", prm.siteURL + "subjectHome/" + str(usr.login_key))

        if settings.DEBUG:
            message_list[block_count] += ((message_subject, new_message, from_email, [get_test_subject_email()]), )   #use for test emails
        else:
            message_list[block_count] += ((message_subject, new_message, from_email, [usr.contact_email]), )

        cnt += 1

    return send_mass_email(block_count, message_list)

def get_test_subject_email():
    '''
    return test subject email account for development
    '''
    prm = Parameters.objects.first()
    return prm.testEmailAccount

def get_from_email():
    '''
    return "from" componet of email
    '''
    return f'"{settings.EMAIL_HOST_USER_NAME}" <{settings.EMAIL_HOST_USER }>'

def send_mass_email(block_count, message_list):
    '''
    send list of emails
    block_count: chunk size to send emails at
    message_list: list of email messages to send
    '''
    logger = logging.getLogger(__name__)
    logger.info("Send mass email to list")

    error_message = ""
    mail_count = 0

    if len(message_list) > 0:
        try:
            for block in range(block_count+1):
                logger.info(f'Sending Block {block+1} of {block_count+1}')
                mail_count += send_mass_mail(message_list[block], fail_silently=False)
        except SMTPException as exc:
            logger.info(f'There was an error sending email: {exc}')
            error_message = str(exc)
    else:
        error_message = "Message list empty, no emails sent."

    return {"mailCount" : mail_count, "errorMessage" : error_message}
