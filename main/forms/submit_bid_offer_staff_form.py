from django import forms

class SubmitBidOfferStaffForm(forms.Form):
    '''
    submit bid or offer form on staff page
    '''
    
    title = forms.CharField(label='ID',
                            widget=forms.TextInput(attrs={"v-bind:disabled":"session.started===false",
                                                          "title":"Examples: s1, b3, s12",
                                                          "style":"font-size:30px;"}))

    amount = forms.DecimalField(label='Amount',
                                min_value=0,
                                widget=forms.TextInput(attrs={"v-bind:disabled":"session.started===false",
                                                              "title":"Examples: 3, 2.25, 10.5",
                                                              "style":"font-size:30px;" }))    


    