'''
staff view
'''
import logging
import json
import uuid

from django.views import View
from django.shortcuts import render
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.db.models import CharField,F, Value
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from main.decorators import user_is_owner

from main.models import Parameters
from main.models import Session
from main.models import HelpDocs

from main.forms import SessionForm
from main.forms import ValuecostForm
from main.forms import PeriodForm
from main.forms import ImportParametersForm


class StaffSessionView(SingleObjectMixin, View):
    '''
    class based staff view
    '''
    template_name = "staff/staff_session.html"
    websocket_path = "staff-session"
    model = Session
    
    @method_decorator(user_is_owner)
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''

        parameters = Parameters.objects.first()

        try:
            session = self.get_object()    
        except ObjectDoesNotExist :
            raise Http404('Session Not Found')

        valuecost_form_ids=[]
        for i in ValuecostForm():
            valuecost_form_ids.append(i.html_name)

        period_form_ids=[]
        for i in PeriodForm():
            period_form_ids.append(i.html_name)

        try:
            help_text = HelpDocs.objects.annotate(rp=Value(request.path,output_field=CharField()))\
                                       .filter(rp__icontains=F('path')).first().text
        except Exception  as e:   
             help_text = "No help doc was found."

        return render(request=request,
                      template_name=self.template_name,
                      context={"channel_key" : uuid.uuid4(),
                               "id" : session.id,
                               "session_form" : SessionForm(),
                               "valuecost_form" : ValuecostForm(),
                               "valuecost_form_ids" : valuecost_form_ids,
                               "period_form" : PeriodForm(),
                               "period_form_ids" : period_form_ids,
                               "import_parameters_form" : ImportParametersForm(user=request.user),                               
                               "websocket_path" : self.websocket_path,
                               "help_text":help_text,
                               "page_key" : f'{self.websocket_path}-{session.id}',
                               "session" : session})
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        '''
        handle post requests
        '''

        logger = logging.getLogger(__name__) 
        session = self.get_object()

        #check for file upload
        try:
            f = request.FILES['file']
        except Exception  as e: 
            logger.info(f'Staff_Session no file upload: {e}')
            f = -1
        
         #check for file upload
        if f != -1:
            return takeFileUpload(f, session)
        else:
            data = json.loads(request.body.decode('utf-8'))
        

        return JsonResponse({"response" :  "fail"},safe=False)

#take parameter file upload
def takeFileUpload(f, session):
    logger = logging.getLogger(__name__) 
    logger.info("Upload file")

    #format incoming data
    v=""

    for chunk in f.chunks():
        v += str(chunk.decode("utf-8-sig"))

    message = ""

    # try:
    if v[0]=="{":
        return upload_parameter_set(v, session)
    else:
        message = "Invalid file format."
    # except Exception as e:
    #     message = f"Failed to load file: {e}"
    #     logger.info(message)       

    return JsonResponse({"session" : session.json(),
                         "message" : message,
                                },safe=False)

#take parameter set to upload
def upload_parameter_set(v, session):
    logger = logging.getLogger(__name__) 
    logger.info("Upload parameter set")
    

    ps = session.parameter_set

    logger.info(v)
    v = eval(v)
    #logger.info(v)       

    message = ps.from_dict(v)

    return JsonResponse({"session" : session.json(),
                         "message" : message,
                                },safe=False)
