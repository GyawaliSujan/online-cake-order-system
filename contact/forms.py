import json
import urllib
from django import forms
from django.core.exceptions import ValidationError

from contact.models import Contact


class ContactForm(forms.ModelForm):
    phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
                             error_messages={'invalid': "Phone number must be entered in\
                                            the format: '+999999999'. Up to 15 digits allowed."})

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']
        # widgets = {        }
