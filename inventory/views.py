from django.shortcuts import render
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