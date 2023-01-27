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



class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ("created_at", "updated_at")
        extra_kwargs = {
            "user": {"read_only": True}
        }


    def validate(self, attrs):
        name = attrs.get("name")

        if "test" in name:
            raise serializers.ValidationError({"error": "What are u doing"})

        return attrs


    def create(self, validated_data):
        print(validated_data)
        name = validated_data.get("name")
        return Product.objects.create(**validated_data)
