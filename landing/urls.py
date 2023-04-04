from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^privacy-policy/$', views.privacy_policy, name='privacy_policy'),
    url(r'^terms-and-conditions/$', views.termsAndConditions, name='terms_and_condition'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^cakes/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        views.CakeDetailView.as_view(), name='product_detail'),
    url(r'^search/', views.CakeSearchView.as_view(), name='product_search'),
    url(r'^cart/$', views.CartPageView.as_view(), name='shoppingcart'),
    url(r'^checkout/$', views.CheckoutView.as_view(), name='checkout'),

    url(r'^message/(?P<page>\w+)/(?P<status>\w+)/$', views.MessagePage.as_view(), name='message_page'),
]
