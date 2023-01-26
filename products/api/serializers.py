from rest_framework import serializers
from ..models import Product, Category
from accounts.models import MyUser as User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    wishlist = UserSerializer(many=True)

    class Meta:
        model = Product
        exclude = ("created_at", "updated_at")