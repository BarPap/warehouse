from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list),
    path('<int:product_id>/', views.product_detail),
    path('add-product/', views.add_product),
    path('edit-product/<int:product_id>/', views.edit_product),
    path('delete-product/<int:product_id>/', views.delete_product),
]