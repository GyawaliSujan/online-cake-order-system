import hashlib
import json

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings

RECEIVER_EMAIL = settings.PAYPAL_EMAIL
PAYPAL_RATE = settings.PAYPAL_RATE


def get_paypal_configs(cart_items, user_id):
    total_price = reduce(lambda total, item: total + item.price, cart_items, 0.0)
    total_price_in_usd = total_price / PAYPAL_RATE

    item_names = ', '.join(map(lambda item: item.product.name + ' (' + str(item.cake_size) + ' lbs)', cart_items))
    invoice = "cakeg_checkout_" + str(cart_items[0].checkout.id)
    custom = json.dumps({
        'checkout_id': cart_items[0].checkout.id,
        'khukuri_rum': get_checksum(cart_items[0].checkout.id, user_id, invoice, RECEIVER_EMAIL, total_price),
    })
    site= Site.objects.get(id=settings.SITE_ID)
    config =  {
        "business": RECEIVER_EMAIL,
        # "amount": "%.2f" % total_price_in_usd,
        # "item_name": item_names,
        "invoice": invoice,
        "notify_url": "http://" + site.domain + reverse('paypal-ipn'),
        "return_url": "http://" + site.domain + reverse('payment.paypal_success',
                                                         args=(cart_items[0].checkout.id,)),
        "cancel_return": "http://" + site.domain + reverse('payment.paypal_failure'),
        "custom": custom,  # Custom command to correlate to some function later (optional)
        "cmd": "_cart",
        "upload": "1",
    }

    for index, cart_item in enumerate(cart_items):
        config['item_name_'+str(index + 1)] = cart_item.product.name
        config['item_number_'+str(index + 1)] = cart_item.id
        config['amount_'+str(index + 1)] = "%.2f" % (cart_item.price / PAYPAL_RATE)
    return config


def get_paypal_form(cart_items, user_id):
    return PayPalPaymentsForm(initial=get_paypal_configs(cart_items, user_id))


def get_checksum(*args):
    total_string = ','.join(map(str, args))+settings.SECRET_KEY
    return hashlib.md5(total_string).hexdigest()

def generate_reference_code_for_paypal(checkout_id):
    reference_code = hashlib.md5(settings.SECRET_KEY + 'paypal' + str(checkout_id)).hexdigest()
    reference_code = 'PPL-'+reference_code[-8:]
    return reference_code

def generate_reference_code_for_COD(checkout_id):
	reference_code = hashlib.md5(settings.SECRET_KEY + 'cod' + str(checkout_id)).hexdigest()
	reference_code = 'COD-'+reference_code[-8:]
	return reference_code