from django.shortcuts import render
from .models import (
    Product, ProductImage, Size, Category
)
from django.db.models import F, FloatField
from django.db.models.functions import Coalesce

# Create your views here.

def product_list_view(request):
    context = {
        "categories": Category.objects.order_by("-created_at"),
        "products": Product.objects.order_by("-created_at"),
        "sizes": Size.objects.order_by("-created_at")
    }
    return render(request, "products/list.html", context)


