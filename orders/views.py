from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from ecommerce.utils.email_sender import send_brevo_email


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # clear the cart
            cart.clear()
            messages.success(request, 'Your order has been placed successfully!')
            return redirect('orders:order_success', order_id=order.id)
    else:
        # Pre-fill form with user data if available
        initial_data = {}
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'address': profile.address,
                'postal_code': profile.postal_code,
                'city': profile.city,
            }
        form = OrderCreateForm(initial=initial_data)
    return render(request, 'cart/checkout.html', {'cart': cart, 'form': form})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()
    # Calculate prices manually
    subtotal = sum(item.price * item.quantity for item in order_items)
    tax = subtotal * Decimal(0.05)
    if subtotal >= 400:
        shipping = Decimal(50)
    else:
        shipping = Decimal(0)
    total = subtotal + tax + shipping
    # Generate item HTML
    items_html = ''.join([
        f"<div class='item'><div>{item.product.name} (Qty: {item.quantity})</div><div>₹{item.price * item.quantity:.2f}</div></div>"
        for item in order_items
    ])
    # Send email to user
    user_subject = f"✅ Order Confirmation - #{order.id}"
    user_message = f"""
    <!DOCTYPE html>
    <html><head> <style>
        body {{ font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; }}
        .card {{ background-color: #fff; max-width: 650px; margin: auto; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.05); }}
        .header {{ display: flex; justify-content: space-between; align-items: center; }}
        .status {{ padding: 5px 10px; border-radius: 5px; color: #fff; font-weight: bold; }}
        .status.pending {{ background-color: #f1c40f; }}
        .status.processing {{ background-color: #3498db; }}
        .status.shipped {{ background-color: #2980b9; }}
        .status.delivered {{ background-color: #2ecc71; }}
        .status.cancelled {{ background-color: #e74c3c; }}
        .item {{ border-bottom: 1px solid #eee; padding: 10px 0; display: flex; justify-content: space-between; }}
        .summary-table {{ width: 100%; margin-top: 10px; border-collapse: collapse; }}
        .summary-table td {{ padding: 6px 0; }}
    </style></head><body>
    <div class="card">
        <div class="header">
            <h2>Order #{order.id}</h2>
        </div>
        <p><strong>Placed on:</strong> {order.created.strftime('%B %d, %Y')}</p>

        <h3>🛍 Items Ordered:</h3>
        {items_html}

        <h3>📦 Delivery Address:</h3>
        <p>
            {order.first_name} {order.last_name}<br>
            {order.address}<br>
            {order.city}, {order.postal_code}
        </p>

        <h3>💰 Order Summary:</h3>
        <table class="summary-table">
            <tr><td>Subtotal:</td><td>₹{subtotal:.2f}</td></tr>
            <tr><td>Tax (5%):</td><td>₹{tax:.2f}</td></tr>
            <tr><td>Shipping:</td><td>₹{shipping:.2f}</td></tr>
            <tr><td><strong>Total:</strong></td><td><strong>₹{total:.2f}</strong></td></tr>
        </table>

        <p>Thank you for shopping with <strong>Sarika Trader</strong>! We’ll notify you when your order ships.</p>
    </div></body></html>
    """
    # Admin email message (reuse style and item HTML)
    admin_subject = f"🛎️ New Order Placed - #{order.id}"
    admin_message = f"""
    <!DOCTYPE html>
    <html><head> <style>
        body {{ font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; }}
        .card {{ background-color: #fff; max-width: 650px; margin: auto; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.05); }}
        .header {{ display: flex; justify-content: space-between; align-items: center; }}
        .status {{ padding: 5px 10px; border-radius: 5px; color: #fff; font-weight: bold; }}
        .status.pending {{ background-color: #f1c40f; }}
        .status.processing {{ background-color: #3498db; }}
        .status.shipped {{ background-color: #2980b9; }}
        .status.delivered {{ background-color: #2ecc71; }}
        .status.cancelled {{ background-color: #e74c3c; }}
        .item {{ border-bottom: 1px solid #eee; padding: 10px 0; display: flex; justify-content: space-between; }}
        .summary-table {{ width: 100%; margin-top: 10px; border-collapse: collapse; }}
        .summary-table td {{ padding: 6px 0; }}
    </style></head><body>
    <div class="card">
        <div class="header">
            <h2>New Order Received - #{order.id}</h2>
        </div>
        <p><strong>Date:</strong> {order.created.strftime('%B %d, %Y')}</p>

        <h3>👤 Customer Info:</h3>
        <p>
            <strong>Name:</strong> {order.user.username}<br>
            <strong>Email:</strong> {order.user.email}
        </p>

        <h3>📦 Delivery Address:</h3>
        <p>
            {order.first_name} {order.last_name}<br>
            {order.address}<br>
            {order.city}, {order.postal_code}
        </p>

        <h3>🛍 Products:</h3>
        {items_html}

        <h3>💰 Price Summary:</h3>
        <table class="summary-table">
            <tr><td>Subtotal:</td><td>₹{subtotal:.2f}</td></tr>
            <tr><td>Tax (5%):</td><td>₹{tax:.2f}</td></tr>
            <tr><td>Shipping:</td><td>₹{shipping:.2f}</td></tr>
            <tr><td><strong>Total:</strong></td><td><strong>₹{total:.2f}</strong></td></tr>
        </table>
        <p>✅ This email was automatically generated by Sarika Trader System.</p>
    </div></body></html>
    """
    # Send emails
    send_brevo_email(user_subject, user_message, [order.user.email])
    send_brevo_email(admin_subject, admin_message, [settings.ADMIN_EMAIL])
    return render(request, 'orders/order_success.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})