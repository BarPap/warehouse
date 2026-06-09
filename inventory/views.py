from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from .forms import ProductForm

def validate_product_form(name, quantity_str):
        errors = {}
        if not name:
            errors['name'] = 'Nazwa nie może być pusta'
        elif len(name) < 3:
            errors['name'] = 'Nazwa nie może być krótsza niż 3 znaki'

        try:
            quantity = int(quantity_str)
            if quantity < 0:
                errors['quantity'] = "Ilość nie może być liczbą ujemną"
        except ValueError:
            errors['quantity'] = "Ilość musi być liczbą całkowitą"
        
        return errors

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "inventory/product_list.html", {"products": products})


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "inventory/product_detail.html", {"product": product})

# @login_required
# def add_product(request):
#     errors = {}

#     if request.method == 'GET':
#         return render(request, "inventory/add_product.html", {'errors': errors})    
    
#     if request.method == 'POST':
#         name = request.POST.get("name", "").strip()
#         quantity_str = request.POST.get('quantity', '').strip()
        
#         errors = validate_product_form(name, quantity_str)


#         if not errors:
#             quantity = int(quantity_str)
#             Product.objects.create(name=name, quantity=quantity)
#             return redirect('product_list')

#     return render(request, "inventory/add_product.html", {
#         'errors': errors,
#         'name': request.POST.get('name', ''),
#         'quantity': request.POST.get('quantity', '')
#     })


@login_required
def add_product(request):
    if request.method == 'GET':
        return render(request, "inventory/add_product.html", {'form': ProductForm()})
    if request.method == 'POST':
        all_data = ProductForm(request.POST)
        if all_data.is_valid():
            all_data.save()
            return redirect('product_list')
    return render(request, "inventory/add_product.html", {'form': all_data})

@login_required
def edit_product(request, product_id):
    producd_from_db = get_object_or_404(Product, id=product_id)
    form = ProductForm(instance=producd_from_db)

    if request.method == 'GET':
        return render(request, 'inventory/edit_product.html', {'form': form})
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=producd_from_db)
        if form.is_valid():           
            form.save()
            return redirect('product_list')
    return render(request, 'inventory/edit_product.html', {'form': form})


# @login_required
# def edit_product(request, product_id):
#     errors = {}
#     product = get_object_or_404(Product, id=product_id)

#     if request.method == 'GET':
#         return render(request, 'inventory/edit_product.html', {'errors': errors, 'product': product})
    
#     if request.method == 'POST':
#         name = request.POST.get("name", "").strip()
#         quantity_str = request.POST.get("quantity", "").strip()

#         errors = validate_product_form(name, quantity_str)    

#         if not errors:
#             quantity = int(quantity_str)
#             product.name = name
#             product.quantity = quantity
#             product.save()

#             return redirect('product_list')

#     return render(request, "inventory/edit_product.html", {
#         "errors": errors,
#         'name': request.POST.get("name", "").strip(),
#         'quantity': request.POST.get("quantity", "").strip()
#         })

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
