'''
value cost edit form
'''

from django import forms

from main.models import ParameterSetPeriod

class PeriodForm(forms.ModelForm):
    '''
    value cost edit form
    '''
    price_cap = forms.DecimalField(label='Price Cap',
                                    min_value=0,
                                    widget=forms.NumberInput(attrs={"v-model":"session.parameter_set.periods[current_period-1].price_cap",
                                                                    "step":"0.25"}))
    
    price_cap_enabled = forms.ChoiceField(label='Enabled',
                                          choices=((True, 'Yes'), (False,'No' )),
                                          widget=forms.Select(attrs={"v-model":"session.parameter_set.periods[current_period-1].price_cap_enabled"}))

    class Meta:
        model=ParameterSetPeriod
        fields =['price_cap', 'price_cap_enabled']
