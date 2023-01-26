from django.urls import path
from . import views


app_name = "products-api"

urlpatterns = [
    path("list/", views.product_list_view, name="list"),
    path("cat-list/", views.category_list_view, name="cat-list"),
    path("detail/<slug>/", views.product_detail_view, name="detail"),
]