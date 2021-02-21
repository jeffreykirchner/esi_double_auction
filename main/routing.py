'''
web socket routing
'''
from django.urls import re_path

from main.consumers import SubjectConsumer
from main.consumers import SessionListConsumer

#web socket routing
websocket_urlpatterns = [
    re_path(r'ws/subject/(?P<room_name>\w+)/$', SubjectConsumer.as_asgi()),
    re_path(r'ws/sessionList/(?P<room_name>[-\w]+)/', SessionListConsumer.as_asgi()),
]