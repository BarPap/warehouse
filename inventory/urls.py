from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('add-product/', views.ProductCreateView.as_view(), name='add_product'),
    path('edit-product/<pk>/', views.ProductUpdateView.as_view(), name='edit_product'),
    path('delete-product/<pk>/', views.ProductDeleteView.as_view(), name='delete_product'),
    path('api/products/', views.product_list_api, name='product_list_api'),
    path('api/product_detail_api/<int:product_id>/', views.product_detail_api, name='product_detail_api'),
]