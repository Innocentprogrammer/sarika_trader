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
            subject = "🎉 Thanks for Subscribing to Sarika Trader!"
            message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            background-color: #f5f8fa;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 40px auto;
            background: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 2px solid #eee;
            padding-bottom: 20px;
        }}
        .header h2 {{
            color: #e67e22;
            margin: 0;
        }}
        .content {{
            padding: 20px 0;
        }}
        .content p {{
            font-size: 16px;
            line-height: 1.6;
        }}
        .button {{
            display: inline-block;
            margin-top: 25px;
            padding: 12px 20px;
            background-color: #e67e22;
            color: #fff;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
        }}
        .footer {{
            text-align: center;
            font-size: 13px;
            color: #999;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Welcome to Sarika Trader!</h2>
        </div>
        <div class="content">
            <p>Hi {subscriber.username if hasattr(subscriber, 'username') else 'there'},</p>
            <p>Thank you for subscribing to our newsletter. We're excited to have you with us!</p>
            <p>You’ll now receive the latest updates, market news, and exclusive offers straight to your inbox.</p>
            <a href="https://sarikatrader.com" class="button">Visit Our Website</a>
        </div>
        <div class="footer">
            &copy; 2025 Sarika Trader. All rights reserved.
        </div>
    </div>
</body>
</html>
"""
            send_brevo_email(subject, message, [subscriber.email])

            # Optional: notify admin
            admin_subject = f"📬 New Newsletter Subscriber: {subscriber.email}"
            admin_message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f6f8;
            padding: 0;
            margin: 0;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 30px auto;
            background-color: #ffffff;
            padding: 20px 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        }}
        .header {{
            border-bottom: 1px solid #ddd;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }}
        .header h2 {{
            margin: 0;
            color: #2980b9;
            font-size: 20px;
        }}
        .content p {{
            font-size: 16px;
        }}
        .footer {{
            margin-top: 30px;
            font-size: 13px;
            color: #888;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>New Subscriber Alert 🚀</h2>
        </div>
        <div class="content">
            <p><strong>Email:</strong> {subscriber.email}</p>
            <p>This user has just subscribed to the newsletter.</p>
        </div>
        <div class="footer">
            <p>— Automated Notification from Sarika Trader</p>
        </div>
    </div>
</body>
</html>
"""
            from django.conf import settings
            send_brevo_email(admin_subject, admin_message, [settings.ADMIN_EMAIL])

            messages.success(request, "Thank you for subscribing!")
        else:
            messages.error(request, "Please enter a valid email.")
    return redirect('home')  # or wherever your homepage is