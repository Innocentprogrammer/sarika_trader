import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.contrib.auth.models import User
from ecommerce.utils.email_sender import send_brevo_email


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Email information 
            subject = "🎉 Welcome to Our Ecommerce Site, {{user.username}}!"

            message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f4;
            color: #333;
            padding: 0;
            margin: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 30px auto;
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            text-align: center;
            padding-bottom: 20px;
        }}
        .header h2 {{
            color: #2E86C1;
            margin-bottom: 10px;
        }}
        .content p {{
            font-size: 16px;
            line-height: 1.6;
        }}
        .button {{
            display: inline-block;
            margin-top: 20px;
            padding: 12px 25px;
            background-color: #2E86C1;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            font-size: 13px;
            color: #aaa;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Hi {user.username},</h2>
            <p>🎉 Thanks for joining us at <strong>Our Ecommerce Site</strong>!</p>
        </div>
        <div class="content">
            <p>We're thrilled to have you on board. Explore amazing products, enjoy exclusive deals, and make the most of your shopping experience.</p>
            <p>Start browsing our collection now and discover something special just for you!</p>
            <a href="https://sarika-trader.onrender.com" class="button">Start Shopping 🛍️</a>
        </div>
        <div class="footer">
            <p>&copy; 2025 Our Ecommerce Site. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

            send_brevo_email(subject, message, [user.email])
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
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

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')  # Or any other page like 'login'

def google_login(request):
    google_auth_url = "https://accounts.google.com/o/oauth2/auth"
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
    }

    request_url = f"{google_auth_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
    return redirect(request_url)

def generate_unique_username(base_username):
    """Generate a unique username by appending numbers if needed"""
    username = base_username.lower().replace(' ', '_')  # Clean the username
    
    # Remove any non-alphanumeric characters except underscores
    import re
    username = re.sub(r'[^\w]', '', username)
    
    # Ensure it's not empty
    if not username:
        username = "user"
    
    # Check if username exists and make it unique
    original_username = username
    counter = 1
    
    while User.objects.filter(username=username).exists():
        username = f"{original_username}_{counter}"
        counter += 1
    
    return username

def google_callback(request):
    if "code" not in request.GET:
        return redirect("home")

    code = request.GET["code"]
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
        "code": code,
    }

    token_response = requests.post(token_url, data=data)
    token_data = token_response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        return redirect("home")

    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    email = user_info.get("email")
    name = user_info.get("name", "")
    
    # Extract first name (split by space and take first part)
    first_name = name.split()[0] if name else "user"
    
    # Generate unique username based on first name
    username = generate_unique_username(first_name)
    
    # Check if user already exists by email first
    try:
        user = User.objects.get(email=email)
        # User exists, just log them in
        login(request, user)
    except User.DoesNotExist:
        # Create new user with first name as username
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=" ".join(name.split()[1:]) if len(name.split()) > 1 else "",
            email=email
        )
        # Email information 
        subject = "🎉 Welcome to Our Ecommerce Site, {{user.username}}!"
        message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f4;
            color: #333;
            padding: 0;
            margin: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 30px auto;
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            text-align: center;
            padding-bottom: 20px;
        }}
        .header h2 {{
            color: #2E86C1;
            margin-bottom: 10px;
        }}
        .content p {{
            font-size: 16px;
            line-height: 1.6;
        }}
        .button {{
            display: inline-block;
            margin-top: 20px;
            padding: 12px 25px;
            background-color: #2E86C1;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            font-size: 13px;
            color: #aaa;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Hi {user.username},</h2>
            <p>🎉 Thanks for joining us at <strong>Our Ecommerce Site</strong>!</p>
        </div>
        <div class="content">
            <p>We're thrilled to have you on board. Explore amazing products, enjoy exclusive deals, and make the most of your shopping experience.</p>
            <p>Start browsing our collection now and discover something special just for you!</p>
            <a href="https://sarika-trader.onrender.com" class="button">Start Shopping 🛍️</a>
        </div>
        <div class="footer">
            <p>&copy; 2025 Our Ecommerce Site. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""
        send_brevo_email(subject, message, [user.email])
        login(request, user)

    return redirect("home")