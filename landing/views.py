import json

from django.conf import settings
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.mail import send_mail

from landing.forms import AddToCartForm, CheckoutForm, CartItemForm, DeliveryReceiverForm, DeliveryLocationForm, SecondaryDeliveryReceiverForm
from product.models import Cake, Category, Checkout, CartItem, Holiday
from review.models import Review
from .forms import SearchForm
from contact.forms import ContactForm

from django.contrib import messages


def index(request):
    context = {}
    reviews = Review.objects.all()
    reviews = [tuple(reviews[i:i + 3]) for i in range(0, len(reviews), 3)]
    context = {
        "title": "Cake-G",
        "best_selling_cakes": Cake.objects.best_selling_cakes(),
        "featured_categories": Category.objects.featured_categories(),
        "carousel_categories": Category.objects.carousel_categories(),
        "num_cart_items": len(get_cart_items(request))
    }
    return render(request, 'landing/index.html', context)


def about(request):
    context = {
        'title': 'About'
    }

    return render(request, 'landing/about.html', context)


def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'We will get back to you soon.')
    context = {
        'form': form,
        'title': 'Contact | Cake-G',
    }

    return render(request, 'landing/contact.html', context)


def faq(request):
    context = {
        'title': 'Faq'
    }

    return render(request, 'landing/faq.html', context)

def termsAndConditions(request):
    context = {
        'title': 'Terms and Conditions'
    }
    return render(request, 'landing/terms-and-conditions.html', context=context)


def privacy_policy(request):
    context = {
        'title': 'Privacy Policy'
    }

    return render(request, 'landing/privacy_policy.html', context)


@login_required(login_url="account_login")
def profile(request):
    items_history = CartItem.objects.filter(checkout__client=request.user).select_related()

    context = {
        'title': 'Profile',
        'user': request.user,
        'items_history': items_history
    }


    return render(request, 'landing/profile.html', context)


class CartPageView(View):

    def get(self, request):
        context = {}
        cart_data = get_cart_items(request)
        context['cart_items'] = cart_data
        context['num_cart_items'] = len(cart_data)
        return render(request, 'landing/cart-page.html', context)

    def post(self, request):
        if request.POST.get('removeCartItem', None):
            remove_from_cart(request, request.POST['removeCartItem'])
        return self.get(request)


@method_decorator(login_required, name='dispatch')
class CheckoutView(TemplateView):
    template_name = 'landing/deliveryDetails.html'

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        cart_items = get_cart_items(self.request)

        total_price = reduce(
            lambda a, b: a + b['total_price'], cart_items, 0)

        context['num_cart_items'] = len(cart_items)
        context['total_price'] = total_price
        context['holidays'] = Holiday.objects.get_holidays_formatted()

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['checkoutForm'] = CheckoutForm(prefix='checkout')
        context['cartItemForm'] = CartItemForm(prefix='cartitem')
        context['receiverForm'] = DeliveryReceiverForm(prefix='receiver')
        context['secondaryReceiverForm'] = SecondaryDeliveryReceiverForm(prefix='secondary_receiver')
        context['locationForm'] = DeliveryLocationForm(prefix='location')


        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        checkout_form = CheckoutForm(request.POST, prefix='checkout')
        receiver_form = DeliveryReceiverForm(request.POST, prefix='receiver')
        secondary_receiver_form = SecondaryDeliveryReceiverForm(request.POST, prefix='secondary_receiver')
        location_form = DeliveryLocationForm(request.POST, prefix='location')

        primary_phone = request.POST.get('receiver-phone_number')
        secondary_phone = request.POST.get('secondary_receiver-phone_number')
        if primary_phone == secondary_phone and primary_phone:
            secondary_receiver_form.add_error('phone_number', 'Primary and secondary phone numbers cannot be same.')

        cart_items = get_cart_items_form(request)
        cart_items_are_valid = cart_items and all(
            map(lambda item: item.is_valid(), cart_items))

        if len(cart_items) == 0:
            return HttpResponseRedirect(reverse('product_search'))

        if (cart_items_are_valid
                and receiver_form.is_valid()
                and secondary_receiver_form.is_valid()
                and location_form.is_valid()
                and checkout_form.is_valid()):

            checkout = checkout_form.save_checkout(
                receiver_form,
                secondary_receiver_form,
                location_form,
                checkout_form,
                cart_items,
                request.user
            )

            reset_cart(request)
            return HttpResponseRedirect(reverse("payment_options", kwargs={'checkout_id': checkout.id}))

        context = self.get_context_data(**kwargs)
        context['checkoutForm'] = checkout_form
        context['receiverForm'] = receiver_form
        context['secondaryReceiverForm'] = secondary_receiver_form
        context['locationForm'] = location_form
        context['cart_validity'] = cart_items_are_valid

        return self.render_to_response(context)


EGG_CONTENT_PRICING = {'egg': 0, 'eggless': 100}


class CakeDetailView(DetailView):
    model = Cake
    template_name = "landing/cake-info.html"
    context_object_name = "item_detail"

    def get_context_data(self, **kwargs):
        context = super(CakeDetailView, self).get_context_data(**kwargs)

        recommended_cakes = Cake.objects.cake_recommendations(self.object)
        context['recommended_cakes'] = recommended_cakes

        flavors = json.dumps([{'id': obj.id, 'name': obj.name, 'extraprice': obj.additional_price_per_pound}
                              for obj in self.object.flavor.all()])
        shapes = json.dumps([{'id': obj.id, 'name': obj.name, 'extraprice': obj.additional_price_per_pound}
                             for obj in self.object.shape.all()])
        egg_content = json.dumps(EGG_CONTENT_PRICING)
        context['flavors'] = flavors
        context['shapes'] = shapes
        context['egg_content'] = egg_content


        context['num_cart_items'] = len(get_cart_items(self.request))

        cart_form = AddToCartForm(
            initial={'cake': self.object.id, 'weight': self.object.minsize},
            product=self.object,
        )
        context['cart_form'] = cart_form

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        formData = AddToCartForm(request.POST, product=self.object)
        if (formData.is_valid()):
            self.add_to_cart_session(request, formData.to_json())
            response = HttpResponseRedirect(reverse('shoppingcart'))
            return response
        else:
            context['cart_form'] = formData
            return self.render_to_response(context)

    def add_to_cart_session(self, request, formData):
        jsonShoppingCart = get_cart_items(request)
        jsonShoppingCart.append(formData)
        request.session['ShoppingCart'] = json.dumps(jsonShoppingCart)


class CakeSearchView(ListView):
    model = Cake
    template_name = "landing/cake-list.html"
    paginate_by = 20
    context_object_name = "items"
    form_class = SearchForm

    def get_queryset(self):
        searchForm = SearchForm(self.request.GET)
        try:
            txt = self.request.GET.get('search-txt')
            return self.model.objects.filter(name__icontains=txt)
        except Exception as e:
            pass
        if searchForm.is_valid():
            self.categories = searchForm.cleaned_data['categories']
            if self.categories:
                return self.model.objects.filter(categories__in=self.categories).distinct()
        else:
            raise Http404

        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CakeSearchView, self).get_context_data(**kwargs)

        context['categories'] = Category.objects.all()

        selected_categories = []
        searchForm = SearchForm(self.request.GET)
        if searchForm.is_valid():
            selected_categories = searchForm.cleaned_data['categories']
        context['selected_categories'] = selected_categories

        url_queries = self.request.GET.copy()
        url_queries['page'] = 1					# bogus so that pop doesn't raise error
        url_queries.pop('page')
        url_queries = url_queries.urlencode()
        context['url_parameters'] = url_queries or 'cake-g'

        context['num_cart_items'] = len(get_cart_items(self.request))

        return context


class MessagePage(TemplateView):
    template_name= 'landing/../templates/payment/message-template.html'

    def get_context_data(self, **kwargs):
        page = kwargs.get('page', '')
        status = kwargs.get('status', '')

        success_code = status == 'success'

        context = super(MessagePage, self).get_context_data(**kwargs)
        context['success'] = success_code

        return context


#####################################
#       Helper functions            #
#####################################


def get_kwargs(**kwargs):
    return kwargs


def get_cart_items(request):
    cart_items = request.session.get('ShoppingCart', '[]')
    return json.loads(cart_items)


def get_cart_items_form(request):
    cart_items = get_cart_items(request)
    return [
        CartItemForm(get_kwargs(
            product=item['id'],
            message=item['message_on_cake'],
            cake_size=item['weight'],
            quantity=item['quantity'],
            cake_shape=item['shape'],
            cake_flavor=item['flavor'],
            is_eggless=item['is_eggless'],
            price=item['total_price']
        )) for item in cart_items
    ]


def remove_from_cart(request, cartIndex):
    cart_items = get_cart_items(request)
    try:
        cartIndex = int(cartIndex)
        cart_items = cart_items[:cartIndex] + cart_items[cartIndex + 1:]
        request.session['ShoppingCart'] = json.dumps(cart_items)
    except ValueError:
        raise Http404("Cart Item doesn't exist")


def reset_cart(request):
    request.session['ShoppingCart'] = '[]'
