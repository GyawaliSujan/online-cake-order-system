import json
import urllib
import datetime
from django import forms
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
import pytz

from product.models import Category, Cake, CakeFlavor, CakeShape, Checkout, DeliveryLocation, DeliveryReceiver, \
    CartItem, Holiday


class SearchForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(queryset=None, required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        self.fields['categories'].queryset = Category.objects.all()


class AddToCartForm(forms.Form):
    '''
    initialize as below
    formData = AddToCartForm(request.POST, product=self.object)
    '''
    cake = forms.ModelChoiceField(
        queryset=Cake.objects.filter(), widget=forms.HiddenInput(), required=False)
    cake_type = forms.ChoiceField(choices=[(
        'Egg', 'Egg'), ("Eggless", "Eggless")], initial='Egg', widget=forms.RadioSelect())
    weight = forms.FloatField(min_value=1, widget=forms.TextInput(
        attrs={'class': "form-control input-number", 'style': "text-align: center;"}))
    quantity = forms.IntegerField(min_value=1, widget=forms.TextInput(
        attrs={'class': 'form-control input-number', 'style': "text-align: center;"}), initial=1, required=False)
    flavor = forms.ModelChoiceField(queryset=CakeFlavor.objects.none(
    ), widget=forms.Select(attrs={'class': 'custom-select form-control'}))
    shape = forms.ModelChoiceField(queryset=CakeShape.objects.none(
    ), widget=forms.Select(attrs={'class': 'custom-select form-control'}))
    message_on_cake = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Message on Cake..', 'rows':3}))

    def __init__(self, *args, **kwargs):
        product_obj = kwargs.pop('product')
        super(AddToCartForm, self).__init__(*args, **kwargs)
        self.fields['flavor'].queryset = product_obj.flavor
        self.fields['shape'].queryset = product_obj.shape
        self.fields['weight'] = forms.FloatField(min_value=product_obj.minsize, widget=forms.TextInput(
            attrs={'class': "form-control input-number", 'style': "text-align: center;"}))

    def to_json(self):
        # call is_valid before usage
        cleaned = self.cleaned_data
        cake = self.cleaned_data['cake']
        return {
            'id': self.cleaned_data['cake'].id,
            'name': self.cleaned_data['cake'].name,
            'image': self.cleaned_data['cake'].image.url,
            'basePrice': self.cleaned_data['cake'].price,
            'cake_type': self.cleaned_data['cake_type'],
            'is_eggless': self.cleaned_data['cake_type']=='Eggless',
            'weight': self.cleaned_data['weight'],
            'quantity': self.cleaned_data['quantity'],
            'flavor': self.cleaned_data['flavor'].id,
            'flavor_name': self.cleaned_data['flavor'].name,
            'shape': self.cleaned_data['shape'].id,
            'shape_name': self.cleaned_data['shape'].name,
            'message_on_cake': self.cleaned_data['message_on_cake'],
            'total_price': self.get_total_cost()
        }

    def get_total_cost(self):
        basePrice = self.cleaned_data['cake'].price
        flavorPrice = self.cleaned_data['flavor'].additional_price_per_pound
        shapePrice = self.cleaned_data['shape'].additional_price_per_pound

        weight = self.cleaned_data['weight']
        quantity = self.cleaned_data['quantity']

        totalPrice = (basePrice + flavorPrice + shapePrice) * weight * quantity
        return totalPrice


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        exclude = ['items', 'delivery_location', 'receiver', 'secondary_receiver', 'client', 'status']
        widgets = {
            'message': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }

    @transaction.atomic
    def save_checkout(self, receiver_form, secondary_receiver_form, location_form, checkout_form, cart_items, user_obj):
        receiver = receiver_form.save()
        secondary_receiver = secondary_receiver_form.save()
        location = location_form.save()

        checkout = checkout_form.save(commit=False)
        checkout.delivery_location = location
        checkout.receiver = receiver
        checkout.secondary_receiver = secondary_receiver
        checkout.client = user_obj
        checkout.status = 'pending'
        checkout.save()

        for cart_item in cart_items:
            cart_item.save(commit=False)
            ### this should just be temporary hack. please find implcations of updating instance directly
            cart_item.instance.checkout = checkout
            cart_item.save()

        return checkout

    def clean(self):
        cleaned_data = super(CheckoutForm, self).clean()
        delivery_date = cleaned_data['delivery_time']
        NPT = pytz.timezone('Asia/Kathmandu')
        if (delivery_date < timezone.now()):
            self.add_error('delivery_time', 'Delivery Date cannot be set back to past!!')
        if (datetime.time(11, 0, tzinfo=NPT) > delivery_date.time() > datetime.time(18, 0, tzinfo=NPT)):
            self.add_error('delivery_time', 'Delivery Time should be in between 10 am to 5 pm!')
        if (Holiday.objects.is_holiday(delivery_date.date())):
            self.add_error('delivery_time', 'You can\'t place order on Holidays!')

        return cleaned_data

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        exclude = ['checkout']

class DeliveryReceiverForm(forms.ModelForm):
    class Meta:
        model = DeliveryReceiver
        fields = '__all__'

class SecondaryDeliveryReceiverForm(forms.ModelForm):
    class Meta:
        model = DeliveryReceiver
        fields = '__all__'

class DeliveryLocationForm(forms.ModelForm):
    class Meta:
        model = DeliveryLocation
        fields = '__all__'

