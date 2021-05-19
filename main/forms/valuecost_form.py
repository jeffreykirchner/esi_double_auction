'''
value cost edit form
'''

from django import forms

from main.models import ParameterSetPeriodSubjectValuecost

class ValuecostForm(forms.ModelForm):
    '''
    value cost edit form
    '''
    value_cost = forms.DecimalField(label='Amount',
                                    min_value=0,
                                    widget=forms.NumberInput(attrs={"v-model":"current_valuecost.value_cost",
                                                                    "step":"0.25"}))
    
    enabled = forms.ChoiceField(label='Enabled',
                                choices=((True, 'Yes'), (False,'No' )),
                                widget=forms.Select(attrs={"v-model":"current_valuecost.enabled"}))

    class Meta:
        model=ParameterSetPeriodSubjectValuecost
        fields =['value_cost', 'enabled']
