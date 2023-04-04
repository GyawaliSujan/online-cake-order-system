from django.shortcuts import render
from django.http import HttpResponse
from utils.access_control import admin_only_access

from .forms import CategoryForm, CakeForm


@admin_only_access
def add_category(request):
    form = CategoryForm(request.POST or None)

    if form.is_valid():
        form.save()

    context = {
        'form': form
    }
    return render(request, 'admin/add_category.html', context)


@admin_only_access
def add_product(request):
    form = CakeForm(request.POST or None)

    if form.is_valid():
        form.save()

    context = {
        'form': form
    }
    return render(request, 'admin/product_upload.html', context)
