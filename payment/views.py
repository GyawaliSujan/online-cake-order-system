from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http.response import Http404, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.conf import settings
import braintree
from django.template.context import Context
from django.template.loader import get_template, render_to_string

from payment.paypal_utils import get_paypal_form
from product.models import Checkout


braintree.Configuration.configure(braintree.Environment.Sandbox,
	merchant_id=settings.BRAINTREE_MERCHANT_ID,
	public_key=settings.BRAINTREE_PUBLIC_KEY,
	private_key=settings.BRAINTREE_PRIVATE_KEY
)


def braintree_payment(request):
	client_token = braintree.ClientToken.generate()
	context = {
		'client_token': client_token
	}
	if request.method == 'POST':
		result = braintree.Transaction.sale({
			"amount": 10,
			"payment_method_nonce": request.POST['payment_method_nonce'],
			"options": {
				"submit_for_settlement": False
			}
		})
		if result.is_success:
			context['success']= 'You just paid 10 dollar for the product'
		else:
			context['error']= 'Transaction failed'
	return render(request, 'payment/braintree.html', context)


@login_required
def payment_options(request, checkout_id):
	context = {}
	cart_items = CartItem.objects.filter(checkout=checkout_id, checkout__client=request.user.id)
	if not cart_items:
		raise Http404("Checkout data missing.")

	# @TODO check for checkout already been paid via paypal
	checkout = cart_items[0].checkout
	receiver = checkout.receiver
	secondary_receiver = checkout.secondary_receiver
	location = checkout.delivery_location

	context['checkout'] = checkout
	context['receiver'] = receiver
	context['secondary_receiver'] = secondary_receiver
	context['items'] = cart_items
	context['location'] = location
	context['num_cart_items']= len(cart_items)
	context['total_price'] = reduce(lambda total, item: total + item.price, cart_items, 0)
	context['paypal_form'] = get_paypal_form(cart_items, request.user.id)

	return render(request, 'payment/payment_options.html', context)


@login_required
def cash_on_delivery_success(request, checkout_id):
	checkout = get_object_or_404(Checkout, id=checkout_id, client=request.user.id)
	reference_code = generate_reference_code_for_COD(checkout_id)

	try:
		payment, created = PaymentRecord.objects.get_or_create(method='COD', checkout=checkout, reference_code=reference_code, paid=False)
	except IntegrityError:
		return Http404("Payment already confirmed!! Reference code: "+ reference_code)
	if created:
		ctx = {
			'user': request.user,
			'order_type': 'Cash on Delivery'
		}
		message_admin = render_to_string('payment/email/admin.html', ctx)
		message_customer = render_to_string('payment/email/customer.html', ctx)
		send_mail(
			"Order through Cash on Delivery | Cake-G",
			'',
			'',
			settings.NOTIFICATION_EMAILS,
			fail_silently=True,
			html_message=message_admin
		)
		send_mail(
			"Order Success | Cake-G",
			"",
			'',
			[request.user.email],
			fail_silently=True,
			html_message=message_customer
		)
	context = {
		'heading': 'Order Placed Successfully.',
		'message': '''
			Thanks for making business with us. 
			We will be sending you email confirmation shortly.
			'''
	}
	return render(request, 'payment/message-template.html', context)


def paypal_success(request, checkout_id):
	checkout = get_object_or_404(Checkout, id=checkout_id, client=request.user.id)
	reference_code = generate_reference_code_for_paypal(checkout_id)
	try:
		payment, created = PaymentRecord.objects.get_or_create(method='PAYPAL', checkout=checkout,
															   reference_code=reference_code, paid=True)
	except IntegrityError:
		return Http404("Payment already confirmed!! Reference code: " + reference_code)
	if created:
		ctx = {
			'user': request.user,
			'order_type': 'Paypal'
		}
		message_admin = render_to_string('payment/email/admin.html', ctx)
		message_customer = render_to_string('payment/email/customer.html', ctx)
		send_mail(
			"Order through Paypal | Cake-G",
			'',
			'',
			settings.NOTIFICATION_EMAILS,
			fail_silently=True,
			html_message=message_admin
		)
		send_mail(
			"Order Success | Cake-G",
			"",
			'',
			[request.user.email],
			fail_silently=True,
			html_message=message_customer
		)
	context = {
		'heading': 'Payment Successful.',
		'message': '''
			We will be sending you email confirmation shortly.
		'''
	}
	return render(request, 'payment/message-template.html', context)


def paypal_failure(request):
	# @TODO 400 page
	return HttpResponseBadRequest("Something is broken!!! Contact us <a href='//m.me/cake.ghorahi'>here</a>")


from paypal_signal_handler import *


