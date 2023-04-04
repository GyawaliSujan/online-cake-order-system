from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet
from product.api.serializers import CategorySerializer, CakeSerializer
from product.models import Category, Cake


class CategoryViewSet(ModelViewSet):

    model = Category
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CakeViewSet(ModelViewSet):
    model = Cake
    queryset = Cake.objects.all()
    serializer_class = CakeSerializer
