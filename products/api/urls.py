from django.urls import path
from . import views
from . import cb_views


app_name = "products-api"

urlpatterns = [
    # path("list/", views.product_list_view, name="list"),
    # path("cat-list/", views.category_list_view, name="cat-list"),
    # path("detail/<slug>/", views.product_detail_view, name="detail"),
    path("list/", cb_views.ProductListView.as_view(), name="list"),
    path("create/", cb_views.ProductCreateView.as_view(), name="create"),
    path("list-create/", cb_views.ProductListCreateView.as_view(), name="list-create"),
]