'''
web socket routing
'''
from django.urls import re_path

from main.consumers import SubjectConsumer
from main.consumers import StaffHomeConsumer
from main.consumers import StaffSessionConsumer

#web socket routing
websocket_urlpatterns = [
    re_path(r'ws/subject/(?P<room_name>[-\w]+)/$', SubjectConsumer.as_asgi()),
    re_path(r'ws/staff-home/(?P<room_name>[-\w]+)/', StaffHomeConsumer.as_asgi()),
    re_path(r'ws/staff-session/(?P<room_name>[-\w]+)/', StaffSessionConsumer.as_asgi()),
]