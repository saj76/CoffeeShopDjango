from django.contrib import admin

from .models import Product, Customization, Order, CustomizationOptions

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Customization)
admin.site.register(CustomizationOptions)