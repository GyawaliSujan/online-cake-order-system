from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        print ipn_obj
        if ipn_obj.receiver_email != "receiver_email@example.com":
            # Not a valid payment
            return
        if ipn_obj.custom == "Upgrade all users!":
            pass
    else:
        pass


valid_ipn_received.connect(show_me_the_money)

def paypal_sandbox(request):
    paypal_dict = {
        "business": "ganesh.pandey255@gmail.com",
        "amount": "0.01",
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        "notify_url": "http://a42a1427.ngrok.io" + reverse('paypal-ipn'),
        "return_url": "http://a42a1427.ngrok.io/return_url/",
        "cancel_return": "http://a42a1427.ngrok.io/cancel_url/",
        "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, 'paypal_sandbox.html', context=context)

@csrf_exempt
def return_view(request):
    return HttpResponse("success")

def cancel_view(request):
    return HttpResponse('cancelled')