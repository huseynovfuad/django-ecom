from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("list/", views.product_list_view, name="list"),
    path("create/", views.product_create_view, name="create"),
    path("update/<str:slug>/", views.product_update_view, name="update"),
]