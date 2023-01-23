from products.models import Product
from django.shortcuts import get_object_or_404, redirect


def is_owner(view_func):
    def wrapper_func(request, *args, **kwargs):
        obj = get_object_or_404(Product, slug=kwargs.get("slug"))
        if obj.user != request.user:
            return redirect("/")
        return view_func(request, *args, **kwargs)
    return wrapper_func