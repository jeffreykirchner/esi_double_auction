'''
session edit form
'''

from django import forms

from main.models import ParameterSet

class ParameterSetForm(forms.ModelForm):
    '''
    session edit form
    '''
    consent_form_required = forms.TypedChoiceField(label='Require Consent Form', 
                                                   choices=((True, 'Yes'), (False, 'No')),                   
                                                   widget=forms.RadioSelect(attrs={}))

    consent_form = forms.CharField(label='Consent Form Text',
                                   widget=forms.Textarea(attrs={"rows":"15", "cols":"125"}))

    number_of_periods = forms.CharField(label='Number of Periods',
                                        widget=forms.NumberInput(attrs={"addonchange":'True'}))

    class Meta:
        model = ParameterSet
        fields = ['consent_form_required' , 'consent_form', 'number_of_periods']
