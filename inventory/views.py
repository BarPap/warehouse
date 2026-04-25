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

# to jest wersja bez walidacji danych z formularza - wersja ze sprawdzeniem typów, zakresów i logigi jest niżej
# def add_product(request):
#     error = None
#     if request.method == 'GET':
#         return render(request, "inventory/add_product.html", {'error': error})
    
#     if request.method == 'POST':

#         name = request.POST.get("name", '').strip().lower()
#         quantity = request.POST.get('quantity', '').strip().lower()        

#         if not name or not quantity:
#             error = 'pusta nazwa albo brak ilości'
#             context = {'error': error, 'name': name, 'quantity': quantity}
#             return render(request, "inventory/add_product.html", context)
#         else:
#             return redirect('/products/')

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
            return redirect('/products/')

    return render(request, "inventory/add_product.html", {
        'errors': errors,
        'name': request.POST.get('name', ''),
        'quantity': request.POST.get('quantity', '')
    })