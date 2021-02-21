'''
paramters model form
'''
import pytz

from django import forms
from django.forms import ModelChoiceField

from main.models import Parameters

class ParametersForm(forms.ModelForm):
    '''
    paramters model form
    '''
    contact_email = forms.CharField(label='Contact Email Address',
                                    widget=forms.TextInput(attrs={"size":"125"}))

    site_url = forms.CharField(label='Site URL',
                               widget=forms.TextInput(attrs={"size":"125"}))

    test_email_account = forms.CharField(label='Test Email Account',
                                         widget=forms.TextInput(attrs={"size":"125"}))

    invitation_text_subject = forms.CharField(label='Welcome Email, Subject',
                                              widget=forms.TextInput(attrs={"size":"125"}))

    invitation_text = forms.CharField(label='Welcome Email, Text',
                                      widget=forms.Textarea(attrs={"rows":"15", "cols":"125"}))

    cancelation_text_subject = forms.CharField(label='Cancelation Email, Subject',
                                               widget=forms.TextInput(attrs={"size":"125"}))

    cancelation_text = forms.CharField(label='Cancelation Email, Text',
                                       widget=forms.Textarea(attrs={"rows":"15", "cols":"125"}))

    consent_form_required = forms.ChoiceField(label='Consent Form Required',
                                              choices=((True, 'Yes'), (False,'No' )),
                                              widget=forms.Select)

    questionnaire1_required = forms.ChoiceField(label='Pre-Study Questionnaire',
                                                choices=((True, 'Yes'), (False,'No' )),
                                                widget=forms.Select)

    questionnaire2_required = forms.ChoiceField(label='Post-Study Questionnaire',
                                                choices=((True, 'Yes'), (False,'No' )),
                                                widget=forms.Select)

    experiment_time_zone = forms.ChoiceField(label="Study Timezone",
                                             choices=[(tz, tz) for tz in pytz.all_timezones])

    staff_session_help_text = forms.CharField(label='Session Help Text',
                                              widget=forms.Textarea(attrs={"rows":"25", "cols":"125"}))

    staff_home_help_text = forms.CharField(label='Session List Help Text',
                                           widget=forms.Textarea(attrs={"rows":"25", "cols":"125"}))

    channel_key = forms.CharField(label='Socket channel for general site.',
                                  widget=forms.TextInput(attrs={"size":"125"}))

    class Meta:
        model=Parameters
        fields = ('__all__')
