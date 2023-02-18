from django import forms
from .models import Event 
from django.forms.widgets import TextInput
from django.contrib.auth import get_user_model

User = get_user_model()

class loginform(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={
                "placeholder": "Addresse e-mail..",
                "class": "form-control border-success",
            }
        ),)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                "placeholder": "Mot De Pass...",
                "class": "form-control border-success",
            }
        ),)
    
class add_event(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = "__all__"


class UsersForm(forms.Form):
    
    options = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'data-live-search':'true'},),)
    def __init__(self, *args, **kwargs):
        super(UsersForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = ''
#the color form

