from __future__ import unicode_literals

import os
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.utils.html import format_html
from django.utils.text import slugify

from product.model_mixins import SlugMixin


def get_cake_image_path(instance, filename):
    return os.path.join(str(instance.brand), 'cake', str(instance.id), filename)


def get_category_image_path(instance, filename):
    return os.path.join('category', str(instance.id), filename)

def get_category_carousel_image_path(instance, filename):
    return os.path.join('category_carousel', str(instance.id), filename)


class CategoryQuerySet(models.query.QuerySet):

    def featured_categories(self):
        return self.filter(featured=True).exclude(image__exact='').order_by("order")

    def carousel_categories(self):
        return self.filter(carousel=True).exclude(carousel_image__exact='').order_by("order")


class Category(SlugMixin, models.Model):
    name = models.CharField('Category Name', max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField('Cake Image', upload_to=get_category_image_path, blank=True)
    carousel_image = models.ImageField("Carousel Image", upload_to=get_category_carousel_image_path, blank=True )
    featured = models.BooleanField(default=False)
    carousel = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    order = models.PositiveSmallIntegerField(default=1)

    def __unicode__(self):
        return self.name

    objects = CategoryQuerySet.as_manager()


class CakeShape(models.Model):
    name = models.CharField('Cake Shape', max_length=200)
    additional_price_per_pound = models.IntegerField('Extra Charge')

    def __unicode__(self):
        return '{} (+{})'.format(self.name, self.additional_price_per_pound)


class CakeFlavor(models.Model):
    name = models.CharField('Cake Flavor', max_length=200)
    additional_price_per_pound = models.IntegerField('Extra Price')

    def __unicode__(self):
        return '{} (+{})'.format(self.name, self.additional_price_per_pound)


class CakeQuerySet(models.query.QuerySet):

    def best_selling_cakes(self):
        return self.filter(best_selling=True)[:10]

    def cake_recommendations(self, cake):
        return self.filter(categories__in=cake.categories.all())[:4]

    def categorized_by(self, category_name):
        return self.filter(categories__name=category_name)


class Cake(models.Model):
    name = models.CharField('Cake Name', max_length=200)
    #flavor = models.CharField('Cake Flavor', max_length=200, blank=True)
    price = models.IntegerField()
    minsize = models.IntegerField()
    brand = models.CharField('Cake Brand', max_length=200)
    image = models.ImageField('Cake Image', upload_to=get_cake_image_path)
    categories = models.ManyToManyField("Category", related_name="cakes")
    best_selling = models.BooleanField('Best Selling', default=False)
    created_on = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)
    flavor = models.ManyToManyField(CakeFlavor)
    shape = models.ManyToManyField(CakeShape)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-created_on']
        get_latest_by = 'created_on'

    objects = CakeQuerySet.as_manager()

    @property
    def slug(self):
        return slugify(self.name)



class DeliveryLocation(models.Model):
    location = models.CharField('address', max_length=500)

    latitude = models.FloatField()
    longitude = models.FloatField()

    def __unicode__(self):
        return self.location


class DeliveryReceiver(models.Model):
    name = models.CharField('Receiver\'s Fullname', max_length=256)
    phone_number = models.CharField(
        'Receiver\'s phone number',
        max_length=40,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        ]
    )

    def __unicode__(self):
        return '{} ({})'.format(self.name, self.phone_number)


CHECKOUT_STATUS_CHOICES = (
    ('pending', 'pending'),
    ('verified', 'verified'),
    ('delivered', 'delivered'),
    ('rejected', 'rejected'),
)


class Checkout(models.Model):
    created_on = models.DateTimeField(
        'When was cake ordered', auto_now_add=True)

    delivery_time = models.DateTimeField('When to deliver', )
    delivery_location = models.ForeignKey(
        DeliveryLocation, on_delete=models.PROTECT)
    receiver = models.ForeignKey(
        DeliveryReceiver, on_delete=models.PROTECT, related_name="primary_receiver")
    secondary_receiver = models.ForeignKey(
        DeliveryReceiver, on_delete=models.PROTECT, related_name="secondary_receiver")
    message = models.CharField(
        'Remarks', max_length=500)

    client = models.ForeignKey(User, on_delete=models.PROTECT)
    items = models.ManyToManyField(
        Cake, through='CartItem', through_fields=('checkout', 'product'))

    status = models.CharField(
        'Checkout Status', max_length=20, choices=CHECKOUT_STATUS_CHOICES)

    def items_list(self):
        return format_html('<br />'.join(
                [ u'<a href="{}" target="_blank">{} (<span style="color:green">{}lb</span>) \
				(<span style="color:green">Flavor: {}</span>) (<span style="color:green">Quantity: {}</span>) \
				(<span style="color:green">Eggless: {}</span>) (<span style="color:green">Message: {}</span>) \
				(<span style="color:green">Shape: {}</span>) (<span style="color:green">Price: {}</span>)</a>'.format(
                    reverse("product_detail", kwargs={
                            "pk": item.product.id, "slug": slugify(item.product.name)}),
                    item.product.name, item.cake_size, item.cake_flavor, item.quantity,
                    item.is_eggless, item.message, item.cake_shape, item.price
                ) for item in self.cartitem_set.all()
                ]))

    def colored_status(self):
        color_code = {'pending': 'orange', 'verified': 'green',
                      'delivered': 'blue', 'rejected': 'gray'}
        return format_html(
            "<span style='color:{}'>{}</span>".format(
                color_code.get(self.status, 'black'),
                self.status
            )
        )
    colored_status.admin_order_field = 'status'


class CartItem(models.Model):
    product = models.ForeignKey(Cake, on_delete=models.PROTECT)
    checkout = models.ForeignKey(Checkout, on_delete=models.PROTECT)

    message = models.CharField(max_length=256)
    cake_size = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()

    cake_shape = models.ForeignKey(CakeShape, on_delete=models.PROTECT)
    cake_flavor = models.ForeignKey(CakeFlavor, on_delete=models.PROTECT)
    is_eggless = models.BooleanField('Eggless')

    price = models.FloatField()


class HolidayManager(models.Manager):
    def is_holiday(self, date):
        holidays = self.filter(date=date)
        return bool(len(holidays))

    def get_holidays_formatted(self):
        holidays = self.get_holidays()
        return [str(holiday.date) for holiday in holidays]

    def get_holidays(self):
        return self.filter(date__gt=datetime.datetime.now())


class Holiday(models.Model):
    date = models.DateField('Holiday Date')
    remark = models.CharField('Remarks', max_length=100)

    objects = HolidayManager()
