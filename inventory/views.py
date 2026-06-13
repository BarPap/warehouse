from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from .forms import ProductForm
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "inventory/product_list.html", {"products": products})


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "inventory/product_detail.html", {"product": product})


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/add_product.html'
    success_url = reverse_lazy('product_list')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProductForm
    model = Product
    template_name = 'inventory/edit_product.html'
    success_url = reverse_lazy('product_list')


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'GET':
        return render(request, 'inventory/delete_product.html', {'product': product})
    
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    
    return render(request, 'inventory/delete_product.html', {'product': product})

@api_view(['GET', 'POST'])
def product_list_api(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(['GET','PUT', 'DELETE'])
def product_detail_api(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    serializer = ProductSerializer(product)

    if request.method == 'GET':
        return Response(serializer.data)
    
    if request.method == 'DELETE':
        product.delete()
        return Response(status=204)
    
    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(status=400)
