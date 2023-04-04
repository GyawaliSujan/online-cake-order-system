from django.conf.urls import url

from . import views

urlpatterns = [
	#url(r'^payment/braintree/$', views.braintree_payment, name='payment.braintree'),
	url(r'^options/(?P<checkout_id>\w+)/$', views.payment_options, name='payment_options'),

	url(r'^cash_on_delivery/(?P<checkout_id>\w+)/$', views.cash_on_delivery_success, name='payment.cash_on_delivery_success'),
	url(r'^paypal/success/(?P<checkout_id>\w+)/$', views.paypal_success, name='payment.paypal_success'),
	url(r'^paypal/failure/$', views.paypal_failure, name='payment.paypal_failure'),
]