'''
log in user functionality
'''
import json
import logging

from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render
from django.http import JsonResponse

from main.models import Parameters
from main.forms import LoginForm


def login_view(request):
    '''
    log in view
    '''
    logger = logging.getLogger(__name__) 
    
    #logger.info(request)
    
    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))

        if data["action"] == "login":
            return login_function(request,data)

        return JsonResponse({"response" :  "error"},safe=False)

    else:
        logout(request)

        request.session['redirect_path'] = request.GET.get('next','/')

        prm = Parameters.objects.first()

        form = LoginForm()

        form_ids=[]
        for i in form:
            form_ids.append(i.html_name)

        return render(request,'registration/login.html',{"labManager":prm.lab_manager,
                                                         "form":form,
                                                         "form_ids":form_ids})
    
def login_function(request,data):
    '''
    handle login
    '''
    logger = logging.getLogger(__name__) 
    #logger.info(data)

    #convert form into dictionary
    form_data_dict = {}             

    for field in data["formData"]:            
        form_data_dict[field["name"]] = field["value"]
    
    f = LoginForm(form_data_dict)

    if f.is_valid():

        username = f.cleaned_data['username']
        password = f.cleaned_data['password']

        #logger.info(f"Login user {username}")

        user = authenticate(request, username=username.lower(), password=password)

        if user is not None:
            login(request, user) 

            rp = request.session.get('redirect_path','/')        

            logger.info(f"Login user {username} success , redirect {rp}")

            return JsonResponse({"status":"success","redirect_path":rp}, safe=False)
        else:
            logger.warning(f"Login user {username} fail user / pass")
            
            return JsonResponse({"status":"error"}, safe=False)
    else:
        logger.info(f"Login user form validation error")
        return JsonResponse({"status":"validation","errors":dict(f.errors.items())}, safe=False)