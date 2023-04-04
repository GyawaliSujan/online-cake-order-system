from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json

# Create your views here.


def category_cakes(request):
    category = request.GET.get('category')
    arr_category = category.split(',')
    return JsonResponse({'hello': 'hi'})
