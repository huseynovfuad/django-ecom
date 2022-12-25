from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("list/", views.product_list_view, name="list")
]