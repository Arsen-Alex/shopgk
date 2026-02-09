from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from .models import Product, Order
from .Cart import Cart, CartItem
from yookassa import Configuration, Payment
from django.conf import settings
import uuid

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SHOP_KEY

def create_payment(request, product_id):
    product = Product.objects.get(id=product_id)
    
    payment = Payment.create({
        "amount": {
            "value": str(product.price),
            "currency": "RUB"
        },
        "confirmation": {
        "type": "redirect",
        "return_url": "http://127.0.0.1:8000/payment-success/"
        },
        "capture": True,
        "description": f"Оплата {product.name}"
    }, str(uuid.uuid4()))

    payment_id = payment.id
    Order.objects.create(
        product=product,
        payment_id=payment_id,
        status="pending"
    )

    return redirect(payment.confirmation.confirmation_url)

def payment_success(request):
    return render(request, "payment_success.html")

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("product_list")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")

def product_list(request):
    products = Product.objects.all()
    return render(request, "store/product_list.html", {
        "products": products
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "store/product_detail.html", {
        "product": product
    })


def about(request):
    return render(request, "store/about.html")

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    items = cart.items.all()

    total_price = sum(item.get_total_price() for item in items)

    items = CartItem.objects.filter(cart=cart)

    total_price = sum(
        item.product.price * item.quantity
        for item in items
    )

    return render(request, "cart/cart.html", {
        "cart": cart,
        "items": items,
        "total_price": total_price,
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("view_cart")

@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    try:
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect("view_cart")

@login_required
def update_cart_item(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)

    try:
        item = CartItem.objects.get(
            cart=cart,
            product_id=product_id
        )
    except CartItem.DoesNotExist:
        return redirect("view_cart")

    action = request.GET.get('action')

    if action == 'inc':
        item.quantity += 1
        item.save()
    elif action == 'dec':
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
        else:
            item.save()

    return redirect("view_cart")