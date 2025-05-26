from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import google_login, google_callback

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'), 
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path("google/login/", google_login, name="google_login"),
    path("google/login/callback/", google_callback, name="google_callback"),
]