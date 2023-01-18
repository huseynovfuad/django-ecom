from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("list/", views.product_list_view, name="list"),
    path("create/", views.product_create_view, name="create"),
    path("update/<str:slug>/", views.product_update_view, name="update"),
    path("detail/<str:slug>/", views.product_detail_view, name="detail"),
    path("add/comment/", views.add_comment_view, name="add-comment"),
    path("create/wishlist/", views.wishlist_create_view, name="create-wishlist"),
]