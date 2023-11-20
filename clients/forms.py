from django import forms
from django.core.exceptions import ValidationError
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
    
    about_client_attachment = forms.FileField(required=False) 

