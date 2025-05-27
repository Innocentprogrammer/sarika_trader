from decimal import Decimal
from django.conf import settings
from products.models import Product
from .models import Cart as CartModel, CartItem
from django.utils.crypto import get_random_string

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # Setup or fetch DB Cart
        self.user = request.user if request.user.is_authenticated else None
        session_id = self.session.session_key or get_random_string(32)
        self.session_id = session_id
        self.db_cart, _ = CartModel.objects.get_or_create(
            user=self.user if self.user else None,
            session_id=session_id
        )

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
        # Save to DB
        cart_item, created = CartItem.objects.get_or_create(
            cart=self.db_cart, product=str(product.id)
        )
        cart_item.quantity = quantity if override_quantity else cart_item.quantity + quantity
        cart_item.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            # Remove from DB
            CartItem.objects.filter(cart=self.db_cart, product=str(product.id)).delete()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
        self.db_cart.items.all().delete()