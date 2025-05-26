from django.shortcuts import render, redirect
from products.models import Category
from orders.models import Order
from contact.models import Contact
from accounts.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from contact.forms import SubscriberForm
from ecommerce.utils.email_sender import send_brevo_email

def home(request):
    categories = Category.objects.all()
    data={
        'categories':categories
    }
    return render(request,"home.html",data)

@login_required
def history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def address(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/profile.html', context)

def contact(request):
    if request.method == 'POST':
        full_name=request.POST.get('full_name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        country=request.POST.get('country')
        state=request.POST.get('state')
        city=request.POST.get('city')
        pincode=request.POST.get('pincode')
        message=request.POST.get('message')
        con = Contact(full_name=full_name,email=email,phone=phone,address=address,country=country,state=state,city=city,pincode=pincode,message=message)
        con.save()
    return render(request,"contact.html")

def subscribe_newsletter(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            subject = "Thanks for Subscribing to Sarika Trader!"
            message = f"""
            <h2>Welcome!</h2>
            <p>Thank you for subscribing to our newsletter.</p>
            <p>You’ll now receive updates and exclusive offers from us.</p>
            """
            send_brevo_email(subject, message, [subscriber.email])

            # Optional: notify admin
            admin_subject = f"New Newsletter Subscriber: {subscriber.email}"
            admin_message = f"<p>A new user just subscribed to the newsletter: <strong>{subscriber.email}</strong></p>"
            from django.conf import settings
            send_brevo_email(admin_subject, admin_message, [settings.ADMIN_EMAIL])

            messages.success(request, "Thank you for subscribing!")
        else:
            messages.error(request, "Please enter a valid email.")
    return redirect('home')  # or wherever your homepage is