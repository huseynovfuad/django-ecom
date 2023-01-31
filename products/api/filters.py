import django_filters
from products.models import Product


class ProductFilter(django_filters.FilterSet):
    category_name = django_filters.CharFilter(field_name="category__name", lookup_expr="icontains")
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ("category_name", "name")