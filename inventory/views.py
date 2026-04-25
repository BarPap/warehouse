from django.shortcuts import render, redirect
from django.http import HttpResponse


def product_list(request):
    products = [
        {'name': 'Śrubka M8', 'quantity': 100},
        {'name': 'Nakrętka M8', 'quantity': 50},
        {'name': 'Podkładka stalowa', 'quantity': 200},
    ]   
    context = {"products": products}
    return render(request, "inventory/product_list.html", context)

def product_detail(request, product_id):
    return HttpResponse(f"Szczegóły produktu nr: {product_id}")

def add_product(request):
    error = None
    if request.method == 'GET':
        return render(request, "inventory/add_product.html", {'error': error})
    
    if request.method == 'POST':

        name = request.POST.get("name", '').strip().lower()
        quantity = request.POST.get('quantity', '').strip().lower()        

        if not name or not quantity:
            error = 'pusta nazwa albo brak ilości'
            context = {'error': error, 'name': name, 'quantity': quantity}
            return render(request, "inventory/add_product.html", context)
        else:
            return redirect('/products/')
    