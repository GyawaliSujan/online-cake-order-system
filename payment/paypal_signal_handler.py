import json
from django.db.utils import IntegrityError
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED
from payment.models import PaymentRecord

from paypal_utils import RECEIVER_EMAIL, get_checksum, generate_reference_code_for_paypal, generate_reference_code_for_COD
from product.models import CartItem


def is_valid_custom_message(custom_message):
    try:
        custom_json_message = json.loads(custom_message)
        return True
    except ValueError, ve:
        return False

def is_valid_ipn_object(ipn_obj):
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        if ipn_obj.receiver_email != RECEIVER_EMAIL:
            return False

        if not is_valid_custom_message(ipn_obj.custom):
            return False

        custom_json_message = json.loads(ipn_obj.custom)
        checkout_id = custom_json_message['checkout_id']

        cart_items = CartItem.objects.filter(checkout=checkout_id).select_related()
        if not cart_items:
            return False

        user_id = cart_items[0].checkout.client_id
        total_price = reduce(lambda total, item: total + item.price, cart_items, 0.0)

        khukuri_rum = get_checksum(checkout_id, user_id, ipn_obj.invoice, RECEIVER_EMAIL, total_price)

        if khukuri_rum != custom_json_message['khukuri_rum']:
            return False

        return True
    return False


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    if not is_valid_ipn_object(sender):
        return

    custom_json_message = json.loads(ipn_obj.custom)
    checkout_id = custom_json_message['checkout_id']

    try:
        payment, created = PaymentRecord.objects.get(method='PAYPAL', checkout_id=checkout_id)
        payment.paid = True
        payment.save()
    except IntegrityError, e:
        raise e

valid_ipn_received.connect(show_me_the_money)