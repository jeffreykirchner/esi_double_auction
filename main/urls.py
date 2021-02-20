'''
URL Patterns
'''

from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required

from django.urls import path
from django.urls import re_path
from main import views

urlpatterns = [

    re_path(r'^admin/login/$', views.login_view),
    path('accounts/login/', views.login_view, name="login"),

    path('', login_required(views.StaffHomeView.as_view())),
    path('subject', views.SubjectView.as_view()),

    #txt
    path('robots.txt', views.RobotsTxt, name='robotsTxt'),
    path('ads.txt', views.AdsTxt, name='adsTxt'),
    path('.well-known/security.txt', views.SecurityTxt, name='securityTxt'),
    path('humans.txt', views.HumansTxt, name='humansTxt'),

    #icons
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico'), name='favicon'),
    path('apple-touch-icon-precomposed.png', RedirectView.as_view(url='/static/apple-touch-icon-precomposed.png'), name='favicon'),
    path('apple-touch-icon.png', RedirectView.as_view(url='/static/apple-touch-icon-precomposed.png'), name='favicon'),
    path('apple-touch-icon-120x120-precomposed.png', RedirectView.as_view(url='/static/apple-touch-icon-precomposed.png'), name='favicon'),
]
