from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework import routers
from product.api import viewsets

api_router = routers.DefaultRouter()

api_router.register('category', viewsets.CategoryViewSet)
api_router.register('cake', viewsets.CakeViewSet)


urlpatterns = [url('^product/api/v1/', include(api_router.urls)),
               ]
