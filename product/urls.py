from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^category/cakes/<$', views.category_cakes, name='category.cakes'),
]
