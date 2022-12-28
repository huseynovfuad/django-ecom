from django.shortcuts import render
from .models import (
    Product, ProductImage, Size, Category
)
from django.db.models import F, FloatField
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from services.filter import ProductFilter
from .forms import ProductForm

# Create your views here.

def product_list_view(request):
    context, query_params = {}, ""
    products = Product.objects.annotate(
            tax_price=Coalesce(F("tax"), 0, output_field=FloatField())
        ).annotate(
            discount_price=Coalesce(F("discount"), 0, output_field=FloatField())
        ).annotate(
            total_price = F("price") + F("tax_price") - F("discount_price")
        ).order_by("-created_at")


    products, query_params = ProductFilter(request, products, query_params).filter_products()

    paginator = Paginator(products, 1)
    page = request.GET.get("page", 1)
    product_list = paginator.get_page(page)


    context["categories"] = Category.objects.order_by("-created_at")
    context["products"] = product_list
    context["paginator"] = paginator
    context["sizes"] = Size.objects.order_by("-created_at")
    context["products_count"] = products.count()
    context["query_params"] = query_params
    return render(request, "products/list.html", context)



def product_create_view(request):
    context = {}
    form = ProductForm(initial={"name": "Fuad"})

    print(request.GET)
    if request.method == "POST":
        print(request.POST)

    context["form"] = form
    return render(request, "products/create.html", context)
