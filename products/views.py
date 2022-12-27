from django.shortcuts import render
from .models import (
    Product, ProductImage, Size, Category
)
from django.db.models import F, FloatField
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator

# Create your views here.

def product_list_view(request):
    context, query_params = {}, {}
    products = Product.objects.annotate(
            tax_price=Coalesce(F("tax"), 0, output_field=FloatField())
        ).annotate(
            discount_price=Coalesce(F("discount"), 0, output_field=FloatField())
        ).annotate(
            total_price = F("price") + F("tax_price") - F("discount_price")
        ).order_by("-created_at")

    print(products.values("sizes"))

    print(request.GET)
    if "category" in request.GET:
        category = request.GET.getlist("category")
        query_params["filter_categories"] = [int(i) for i in category]
        products = products.filter(
            category__id__in= category
        )

    if "size" in request.GET:
        sizes = request.GET.getlist("size")
        query_params["filter_sizes"] = [int(i) for i in sizes]
        repeated_products = products.filter(
            sizes__in=sizes
        )
        products = products.filter(
            id__in=repeated_products.values_list("id", flat=True)
        )

    min_price = request.GET.get("min_price", None)
    max_price = request.GET.get("max_price", None)
    if min_price:
        query_params["min_price"] = min_price
        products = products.filter(
            total_price__gte=min_price
        )

    if max_price:
        query_params["max_price"] = max_price
        products = products.filter(
            total_price__lte=max_price
        )

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


