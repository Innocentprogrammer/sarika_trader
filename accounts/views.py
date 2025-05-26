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
            subject = "Welcome to Our Ecommerce Site!"
            message = f"<h2>Hi {user.username},</h2><p>Thanks for registering.</p>"
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
        subject = "Welcome to Our Ecommerce Site!"
        message = f"<h2>Hi {user.username},</h2><p>Thanks for registering.</p>"
        send_brevo_email(subject, message, [user.email])
        login(request, user)

    return redirect("home")