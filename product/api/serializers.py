from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from product.models import Category, Cake
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name','description')


class CakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cake
