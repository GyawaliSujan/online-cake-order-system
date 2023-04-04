import json
import urllib
from django import forms
from django.core.exceptions import ValidationError

from product.models import Category, Cake


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'description']


class CakeForm(forms.ModelForm):

    class Meta:
        model = Cake
        fields = ['name', 'price', 'minsize', 'brand',
                  'categories', 'flavor', 'shape', 'image']
        widgets = {
            'flavor': forms.Select(),
            'shape': forms.Select(),
            'categories': forms.Select()

        }
