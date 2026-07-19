from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, Wishlist, Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def home(request):
    search = request.GET.get("search")

    if search:
        products = Product.objects.filter(name__icontains=search)
    else:
        products = Product.objects.all()

    return render(request, "home.html", {
        "products": products
    })

@login_required(login_url="login")

def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total
    })

from django.contrib.auth.decorators import login_required
@login_required(login_url="login")
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("home")

def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.delete()
    return redirect("cart")

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, "product_detail.html", {
        "product": product
    })

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login")

    return render(request, "signup.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {
                "error": "Invalid Username or Password"
            })

    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect("home")

from django.shortcuts import get_object_or_404

@login_required(login_url="login")
def increase_quantity(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart.quantity += 1
    cart.save()
    return redirect("cart")


@login_required(login_url="login")
def decrease_quantity(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)

    if cart.quantity > 1:
        cart.quantity -= 1
        cart.save()
    else:
        cart.delete()

    return redirect("cart")

from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if request.method == "POST":

        for item in cart_items:
            Order.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                total=item.product.price * item.quantity
            )

        cart_items.delete()

        return render(request, "success.html")

    return render(request, "checkout.html")

@login_required(login_url="login")
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, "wishlist.html", {"items": items})


@login_required(login_url="login")
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect("wishlist")

@login_required(login_url="login")
def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders.html", {"orders": orders})