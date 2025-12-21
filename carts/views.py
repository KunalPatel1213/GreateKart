from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Variation
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required


# Helper function to get/create session cart_id
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.save()   
    return request.session.session_key


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]    
            try:
                variation = Variation.objects.get(
                    product=product, 
                    variation_category__iexact=key, 
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except:
                pass
    product = get_object_or_404(Product, id=product_id)

    # Get or create Cart
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    # ✅ Check if same product with same variations exists
    cart_items = CartItem.objects.filter(product=product, cart=cart)
    existing_item = None
    for item in cart_items:
        if set(item.variations.all()) == set(product_variation):
            existing_item = item
            break

    if existing_item:
        existing_item.quantity += 1
        existing_item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            for item in product_variation:
                cart_item.variations.add(item)
        cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id, cart_item_id=None):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    # ✅ remove only the correct variation item
    if cart_item_id:
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart, product=product)
    else:
        cart_item = CartItem.objects.filter(product=product, cart=cart).first()

    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id=None):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    if cart_item_id:
        CartItem.objects.filter(id=cart_item_id, product=product, cart=cart).delete()
    else:
        CartItem.objects.filter(product=product, cart=cart).delete()

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100 if total > 0 else 0
        grand_total = total + tax
    except ObjectDoesNotExist:
        cart_items = []  # ensure cart_items is iterable even if empty

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url = 'login')
def checkout(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100 if total > 0 else 0
        grand_total = total + tax
    except ObjectDoesNotExist:
        cart_items = []  # ensure cart_items is iterable even if empty

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render (request, 'store/checkout.html', context)