'''
admin screen models
'''

from django.contrib import admin

from main.forms import ParametersForm

from main.models import Parameters
from main.models import Session

from django.db.models.functions import Lower

class ParametersAdmin(admin.ModelAdmin):
    '''
    parameters model admin
    '''
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    form = ParametersForm

    actions = []

admin.site.register(Parameters, ParametersAdmin)

class SessionAdmin(admin.ModelAdmin):
    '''
    Session model admin
    '''
    def has_add_permission(self, request, obj=None):
        return False

    actions = []
    list_display = ['title', 'creator_string']
    ordering = [Lower('creator__email'), Lower('title')]

    readonly_fields = ('parameter_set','start_date')

admin.site.register(Session, SessionAdmin)
