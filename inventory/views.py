from django.shortcuts import render, redirect, get_object_or_404
from .models import Product


def product_list(request):
    products = Product.objects.all()
    return render(request, "inventory/product_list.html", {"products": products})



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "inventory/product_detail.html", {"product": product})


def add_product(request):
    errors = {}

    if request.method == 'GET':
        return render(request, "inventory/add_product.html", {'errors': errors})    
    
    if request.method == 'POST':
        name = request.POST.get("name", "").strip()
        quantity_str = request.POST.get('quantity', '').strip()

        if not name:
            errors['name'] = 'Nazwa nie może być pusta'
        elif len(name) < 3:
            errors['name'] = 'Nazwa nie może być krótsza niż 3 znaki'
        
        try:
            quantity = int(quantity_str)
            if quantity < 0:
                errors['quantity'] = 'Ilość nie może być liczbą ujemną'
        except ValueError:
            errors['quantity'] = 'Ilość musi być liczbą całkowitą'

        if not errors:
            Product.objects.create(name=name, quantity=quantity)
            return redirect('/products/')

    return render(request, "inventory/add_product.html", {
        'errors': errors,
        'name': request.POST.get('name', ''),
        'quantity': request.POST.get('quantity', '')
    })