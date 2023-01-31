from rest_framework import generics
from rest_framework.response import Response
from .serializers import ProductSerializer, ProductCreateSerializer
from ..models import Product
from .filters import ProductFilter
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .paginations import CustomPagination
from rest_framework.permissions import IsAuthenticated
from .permissions import ReadOnly



class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = CustomPagination
    permission_classes = (ReadOnly, )


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(user=self.request.user)
    #     return Response(serializer.data, status=201)


    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)



class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)