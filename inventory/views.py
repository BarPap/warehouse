from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib.auth.decorators import login_required

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

@login_required
def add_product(request):
    errors = {}

    if request.method == 'GET':
        return render(request, "inventory/add_product.html", {'errors': errors})    
    
    if request.method == 'POST':
        name = request.POST.get("name", "").strip()
        quantity_str = request.POST.get('quantity', '').strip()
        
        errors = validate_product_form(name, quantity_str)


        if not errors:
            quantity = int(quantity_str)
            Product.objects.create(name=name, quantity=quantity)
            return redirect('/products/')

    return render(request, "inventory/add_product.html", {
        'errors': errors,
        'name': request.POST.get('name', ''),
        'quantity': request.POST.get('quantity', '')
    })

@login_required
def edit_product(request, product_id):
    errors = {}
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'GET':
        return render(request, 'inventory/edit_product.html', {'errors': errors, 'product': product})
    
    if request.method == 'POST':
        name = request.POST.get("name", "").strip()
        quantity_str = request.POST.get("quantity", "").strip()

        errors = validate_product_form(name, quantity_str)



        if not errors:
            quantity = int(quantity_str)
            product.name = name
            product.quantity = quantity
            product.save()

            return redirect('/products/')

    return render(request, "inventory/edit_product.html", {
        "errors": errors,
        'name': request.POST.get("name", "").strip(),
        'quantity': request.POST.get("quantity", "").strip()
        })

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'GET':
        return render(request, 'inventory/delete_product.html', {'product': product})
    
    if request.method == 'POST':
        product.delete()
        return redirect('/products/')
    
    return render(request, 'inventory/delete_product.html', {'product': product})