from django.shortcuts import render
from django.http import HttpResponse


def product_list(request):
    return HttpResponse("Lista produktów - w budowie")

def product_detail(request, product_id):
    return HttpResponse(f"Szczegóły produktu nr: {product_id}")