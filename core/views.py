from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Sale

def product_list(request):
    return render(request, "product_list.html", {
        "products": Product.objects.all()
    })

def sale_list(request):
    return render(request, "sale_list.html", {
        "sales": Sale.objects.order_by("-id")
    })

def create_sale(request):
    products = Product.objects.all()

    if request.method == "POST":
        product = Product.objects.get(id=request.POST["product"])
        quantity = int(request.POST["quantity"])
        Sale.objects.create(product=product, quantity=quantity)
        return redirect("sale_list")

    return render(request, "create_sale.html", {"products": products})


def delete_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    sale.delete()
    return redirect("sale_list")
