'''
staff view
'''
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import JsonResponse

class SubjectView(TemplateView):
    '''
    class based staff view
    '''
    template_name = "subject_home.html"

    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''

        return render(request, self.template_name, {"id":""})
    

    def post(self, request, *args, **kwargs):
        '''
        handle post requests
        '''
        
        return JsonResponse({"response" : "fail"}, safe=False)