from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
    path("sales/", views.sale_list, name="sale_list"),
    path("sales/new/", views.create_sale, name="create_sale"),
    path("sales/delete/<int:pk>/", views.delete_sale, name="delete_sale"),
]