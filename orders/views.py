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

    # Send email to user
    user_subject = "Your Order Has Been Placed!"
    user_message = f"""
    <h2>Hi {order.user.username},</h2>
    <p>Your order <strong>#{order.id}</strong> was successful.</p>
    <p>We'll deliver your products soon.</p>
    """
    send_brevo_email(user_subject, user_message, [order.user.email])

    # Send email to admin
    admin_subject = f"New Order Received: #{order.id}"
    admin_message = f"""
    <h2>New Order Received</h2>
    <p><strong>Customer:</strong> {order.user.username} ({order.user.email})</p>
    <p><strong>Order ID:</strong> {order.id}</p>
    <p><strong>Products:</strong></p>
    <ul>
    {''.join([f"<li>{item.product.name} (Qty: {item.quantity})</li>" for item in order.items.all()])}
    </ul>
    """
    send_brevo_email(admin_subject, admin_message, [settings.ADMIN_EMAIL])
    return render(request, 'orders/order_success.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})