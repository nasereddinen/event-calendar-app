from django import forms
from .models import Event , ColorEvent
from django.forms.widgets import TextInput

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

#the color form

class ColorForm(forms.ModelForm):
    
    
    class Meta:
        model = ColorEvent
        fields = "__all__"
        widgets = {
            "color": TextInput(attrs={"type": "color"}),
        }