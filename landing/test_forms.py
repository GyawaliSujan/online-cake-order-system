from django.test import TestCase
from .forms import CheckoutForm, DeliveryLocationForm, DeliveryReceiverForm, CartItemForm
from product.models import DeliveryLocation, DeliveryReceiver


class DeliveryLocationTest(TestCase):
    fixtures = ["cakeg/landing/fixtures/fixtures_for_test.json"]
    def setup(self):
        pass
    def test_invalid_location(self):
        receiver = DeliveryLocationForm({
            "location": 'mdlkerjlkdfs sf',
            "latitude": "kdlsfaj",
            "logitude": "lskfdaslkf",
        })

        self.assertEqual(receiver.is_valid(), False)

    def test_valid_location(self):
        receiver = DeliveryLocationForm({
            "location": 'mdlkerjlkdfs sf',
            "latitude": 27.24563,
            "longitude": 84.25665,
            "client": 1
        })

        self.assertEqual(receiver.is_valid(), True)


class DeliveryReceiverTest(TestCase):
    fixtures = ["cakeg/landing/fixtures/fixtures_for_test.json"]
    def setup(self):
        pass
    def test_invalid_location(self):
        receiver = DeliveryReceiverForm({
            "name": 'mdlkerjlkdfs sf',
            "phone_number": "4353kdlsfaj",
        })

        self.assertEqual(receiver.is_valid(), False)

    def test_valid_location(self):
        receiver = DeliveryReceiverForm({
            "name": 'mdlkerjlkdfs sf',
            "phone_number": "123456799",
        })

        self.assertEqual(receiver.is_valid(), True)


def getKwargs(**kwargs):
    return kwargs

class CheckoutTest( TestCase ):
    fixtures = ["cakeg/landing/fixtures/fixtures_for_test.json"]
    def setup(self):
        print "hello"
        DeliveryReceiver.objects.create(
            name='mdlkerjlkdfs sf',
            phone_number="123456799"
        )
        DeliveryLocationForm(getKwargs(
            location='mdlkerjlkdfs sf',
            latitude=27.24563,
            longitude=84.25665
        )).save()



    def test_valid_checkout_form(self):
        # print DeliveryLocationForm(getKwargs(
        #     location='mdlkerjlkdfs sf',
        #     latitude=27.24563,
        #     longitude=84.25665,
        #     client=1
        # )).save()
        # print DeliveryLocation.objects.all()
        # print DeliveryReceiver.objects.all()
        self.setup()

        # cartitems = [CartItemForm(getKwargs(
        #     product=1,
        #     message="happy birthday",
        #     cake_size=3,
        #     quantity=1,
        #     cake_shape=1,
        #     cake_flavor=1,
        # )).save()]

        # a = CartItemForm(getKwargs(
        #     product=1,
        #     message="happy birthday",
        #     cake_size=3,
        #     quantity=1,
        #     cake_shape=1,
        #     cake_flavor=1,
        # ))
        # print a.errors
        # cartItems = a

        checkout = CheckoutForm({
            'delivery_time': '2017-02-12 13:30',
            'delivery_location': DeliveryLocation.objects.all()[0].id,
            'receiver': DeliveryReceiver.objects.all()[0].id,
            'message': "this is test message",
            'client': 1,
            # 'items': cartitems
        })

        if checkout.is_valid():
            checkoutobj = checkout.save()

            a = CartItemForm(getKwargs(
                product=1,
                checkout=checkoutobj,
                message="happy birthday",
                cake_size=3,
                quantity=1,
                cake_shape=1,
                cake_flavor=1,
            ))


            if (a.is_valid()):
                print "cartItem is valid"
                a.save()


        print checkout.errors
        self.assertEqual(checkout.is_valid(), True)
        pass