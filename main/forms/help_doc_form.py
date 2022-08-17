from tinymce.widgets import TinyMCE

from django import forms

from main.models import HelpDocs


class HelpDocForm(forms.ModelForm):


    title = forms.CharField(label='Title',
                                         widget=forms.TextInput(attrs={"size":"125"}))

    text = forms.CharField(label='Text',
                          widget=TinyMCE(attrs={"rows":20, "cols":200, "plugins": "link image code"}))

    class Meta:
        model=HelpDocs
        fields = ('__all__')