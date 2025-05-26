from django.contrib import admin
from contact.models import Contact,Subscriber


# Register your models here.
class contactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'address', 'message')


admin.site.register(Contact, contactAdmin)

class subscribeAdmin(admin.ModelAdmin):
    list_display = ('email','subscribed_at')

admin.site.register(Subscriber,subscribeAdmin)