from rest_framework.response import Response
from ..models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.decorators import api_view


@api_view(["GET", "POST"])
def product_list_view(request):

    if request.method == "GET":
        products = Product.objects.order_by("-created_at")
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=200)

    elif request.method == "POST":
        serializer = ProductSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def product_detail_view(request, slug):

    if request.method == "GET":
        obj = Product.objects.get(slug=slug)
        serializer = ProductSerializer(obj)
        return Response(serializer.data, status=200)

    if request.method == "PUT" or request.method == "PATCH":
        obj = Product.objects.get(slug=slug)
        serializer = ProductSerializer(request.data, instance=obj)
        return Response(serializer.data, status=201)

    if request.method == "DELETE":
        obj = Product.objects.get(slug=slug)
        obj.delete()
        return Response({"message": "Successfully deleted!"})



@api_view(["GET"])
def category_list_view(request):

    if request.method == "GET":
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=200)