from __future__ import unicode_literals

from django.db import models

# Create your models here.
from product.models import Checkout

PAYMENT_METHODS = (
    ('COD', 'Cash on Delivery'),
    ('PAYPAL', 'Paypal'),
)

class PaymentRecord(models.Model):
    method =models.CharField("Payment method", max_length=10, choices=PAYMENT_METHODS)
    checkout = models.OneToOneField(Checkout, on_delete=models.PROTECT, related_name="payment_method")
    reference_code = models.CharField('Reference Code', max_length=100, default="")
    paid = models.BooleanField('Payment Received')

    def __unicode__(self):
        return "Method: {}, Reference Code: {}, Paid: {}".format(self.method, self.reference_code, self.paid)
