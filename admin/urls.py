from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add/product/', views.add_product, name='admin.add_product'),
    url(r'^add/category/', views.add_category, name='admin.add_category'),
]
