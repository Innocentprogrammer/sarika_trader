# 🛒 Django E-Commerce Web Application

This is a full-featured E-Commerce website built using Django. It supports user registration, product listings, shopping cart functionality, order processing, and a contact form.

---

## ✅ Features

- 🔐 User Registration, Login, Profile Management
- 🛍️ Product Listing & Detail View
- 🛒 Shopping Cart with Checkout
- 📦 Order History & Confirmation Pages
- 📧 Contact Form with Email Integration
- 🧾 Newsletter Subscription with Email Support
- 🧩 Modular Django App Structure
- 🖼️ Media Handling for Product & Category Images
- 🎨 Custom Template Design
- 🗂️ Admin Panel Management

---

## 📁 Project Structure

```
E Commerce
├─ .env
├─ .gitignore
├─ accounts
│  ├─ admin.py
│  ├─ apps.py
│  ├─ forms.py
│  ├─ models.py
│  ├─ management
│  |  ├─ __init__.py
│  │  └─ commands
│  │     ├─ __init__.py
│  │     └─ create_superuser.py
│  ├─ signals.py
│  ├─ templates
│  │  └─ accounts
│  │     ├─ login.html
│  │     ├─ profile.html
│  │     └─ register.html
│  ├─ tests.py
│  ├─ urls.py
│  ├─ views.py
│  └─ __init__.py
├─ cart
│  ├─ admin.py
│  ├─ apps.py
│  ├─ cart.py
│  ├─ context_processors.py
│  ├─ forms.py
│  ├─ models.py
│  ├─ templates
│  │  └─ cart
│  │     ├─ cart.html
│  │     └─ checkout.html
│  ├─ tests.py
│  ├─ urls.py
│  ├─ views.py
│  └─__init__.py
├─ contact
│  ├─ admin.py
│  ├─ apps.py
│  ├─ forms.py
│  ├─ models.py
│  ├─ tests.py
│  ├─ views.py
│  └─ __init__.py
├─ db.sqlite3
├─ ecommerce
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ utils
│  │  ├─ email_sender.py
│  ├─ views.py
│  ├─ wsgi.py
│  └─ __init__.py
├─ env
│  ├─ Include
│  ├─ Lib
│  ├─ pyvenv.cfg
│  └─ Scripts
├─ manage.py
├─ media
│  ├─ categories
│  └─ products
├─ orders
│  ├─ admin.py
│  ├─ apps.py
│  ├─ forms.py
│  ├─ models.py
│  ├─ templates
│  │  └─ orders
│  │     ├─ order_history.html
│  │     └─ order_success.html
│  ├─ tests.py
│  ├─ urls.py
│  ├─ views.py
│  └─ __init__.py
├─ products
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ templates
│  │  └─ products
│  │     ├─ product_detail.html
│  │     └─ product_list.html
│  ├─ tests.py
│  ├─ urls.py
│  ├─ views.py
│  └─__init__.py
├─ Procfile
├─ requirements.txt
├─ static
│  ├─ css
│  │  └─ styles.css
│  ├─ images
│  └─ js
│     └─ main.js
└─ templates
   ├─ about.html
   ├─ base.html
   ├─ contact.html
   ├─ home.html
   └─ includes
      ├─ footer.html
      └─ navbar.html
```

---

## 🚀 Getting Started

### 1. Clone the repository

git clone https://github.com/your-username/ecommerce-django.git
cd ecommerce-django

### 2. Create a virtual environment

python -m venv env

### 3. Activate the virtual environment

On Windows:
env\Scripts\activate

or

On Linux/Mac:
source env/bin/activate

### 4. Install dependencies

pip install -r requirements.txt

### 5. Make and Run migrations

python manage.py makemigrateions
python manage.py migrate

### 6. Create a .env file

Which includes:

- #Django Settings
- #Google OAuth Setting
- #Email Notification Setting
- #Razorpay Settings (for payments)

### 7. Create a superuser (admin)

python manage.py createsuperuser

### 8. Run the server

python manage.py runserver

Then open http://127.0.0.1:8000 in your browser.

---

📬 Contact
For questions, suggestions, or contributions, feel free to reach out or create a pull request.
