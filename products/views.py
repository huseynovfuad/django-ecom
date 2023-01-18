from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Product, ProductImage, Size, Category, Comment
)
from django.db.models import F, FloatField
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from services.filter import ProductFilter
from .forms import ProductForm
from django.contrib import messages
from django.http import JsonResponse

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

    paginator = Paginator(products, 10)
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
    form = ProductForm()

    if request.method == "POST":
        print("POST DATA: ", request.POST)
        print("FILES DATA: ", request.FILES)
        form = ProductForm(request.POST or None)
        files = request.FILES.getlist("image")
        if form.is_valid() and len(files)>=1:
            new_product = form.save()
            for file in files:
                ProductImage.objects.create(
                    product=new_product,
                    image=file
                )
            messages.success(request, f"{new_product.name} added!")
            return redirect("products:create")

    context["form"] = form
    return render(request, "products/create.html", context)


def product_update_view(request, slug):
    context = {}
    product = get_object_or_404(Product, slug=slug)
    form = ProductForm(instance=product)

    if request.method == "POST":
        print("POST DATA: ", request.POST)
        # print("FILES DATA: ", request.FILES)
        form = ProductForm(request.POST or None, instance=product)
        files = request.FILES.getlist("image")
        deleted_image_ids = request.POST.get("delete_image_ids")

        print("deleted image ids: ", deleted_image_ids)
        if form.is_valid():
            form.save()

            for file in files:
                ProductImage.objects.create(
                    product=product,
                    image=file
                )

            if deleted_image_ids:
                image_id_list = deleted_image_ids.split(",")
                ProductImage.objects.filter(product=product, id__in=image_id_list).delete()

            return redirect("products:update", slug=product.slug)

    context['product'] = product
    context['form'] = form
    return render(request, "products/update.html", context)



def product_detail_view(request, slug):
    context = {}
    product = get_object_or_404(Product, slug=slug)
    comments = Comment.objects.filter(product=product,parent__isnull=True)
    context["product"] = product
    context["comments"] = comments
    return render(request, "products/detail.html", context)



def add_comment_view(request):
    product_id = request.POST.get("product_id", None)
    comment_id = request.POST.get("comment_id", None)
    comment = request.POST.get("comment", None)


    comment_obj = Comment(
        user=request.user, product=get_object_or_404(Product, id=int(product_id)),
        comment=comment
    )
    if comment_id:
        comment_obj.parent = get_object_or_404(Comment, id=int(comment_id))
    comment_obj.save()

    data = {
        "user": request.user.email,
        "comment": comment,
        "comment_id": comment_id
    }

    return JsonResponse(data)



def wishlist_create_view(request):
    data = {}
    product_obj = get_object_or_404(Product, id=int(request.POST.get("product_id")))

    data["success"] = True
    if request.user in product_obj.wishlist.all():
        product_obj.wishlist.remove(request.user)
        data["success"] = False
    else:
        product_obj.wishlist.add(request.user)
    return JsonResponse(data)