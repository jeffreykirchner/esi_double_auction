'''
web socket routing
'''
from django.urls import re_path

from main.consumers import SubjectConsumer

#web socket routing
websocket_urlpatterns = [
    re_path(r'ws/subject/(?P<room_name>\w+)/$', SubjectConsumer.as_asgi()),
]