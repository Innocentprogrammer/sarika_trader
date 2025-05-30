from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid', 'status',
                    'created', 'updated']
    list_filter = ['paid', 'status', 'created', 'updated']
    inlines = [OrderItemInline]
    search_fields = ['user__username', 'first_name', 'last_name', 'email']