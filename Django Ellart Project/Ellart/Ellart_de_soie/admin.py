from django.contrib import admin
from .models import Product, Profile, Cart

# Admin configuration for the Product model
class ProductAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view
    list_display = ('name', 'price', 'p_details', 'category', 'is_active', 'pimage')

    # Add search functionality on these fields
    search_fields = ('name', 'p_details', 'category')

    # Enable filtering options in the list view
    list_filter = ('category', 'is_active')

    # Add ordering functionality in the admin interface
    ordering = ('name', 'price')

# Register the Product model with the ProductAdmin configuration
admin.site.register(Product, ProductAdmin)

# Admin configuration for the Profile model
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('Username', 'Email', 'Phone')

# Register the Profile model with the ProfileAdmin configuration
admin.site.register(Profile, ProfileAdmin)

# Admin configuration for the Cart model
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')

# Register the Cart model with the CartAdmin configuration
admin.site.register(Cart, CartAdmin)





