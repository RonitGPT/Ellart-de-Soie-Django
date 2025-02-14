from django.db import models
from django.contrib.auth.models import User

# Profile model
class Profile(models.Model):
    Username = models.CharField(max_length=30, verbose_name="Username")
    Email = models.EmailField(max_length=30, verbose_name="Email", default="noemail@example.com")
    Phone = models.IntegerField(verbose_name="Phone")
    Password = models.CharField(max_length=20, verbose_name="Password")
    Confirm_Password = models.CharField(max_length=20, verbose_name="Confirm Password")

    def __str__(self):
        return self.user.username


# Product model
class Product(models.Model):
    CATEGORY_CHOICES = [
        (1, "Baby"),
        (2, "Hair"),
        (3, "Perfumes"),
        (4, "Mens"),
        (5, "Skin"),
        (6, "Women"),
    ]

    name = models.CharField(max_length=50, verbose_name="Product Name")
    price = models.FloatField(verbose_name="Product Price")
    p_details = models.CharField(max_length=500, verbose_name="Product Details")   
    category = models.IntegerField(verbose_name="Product Category", choices=CATEGORY_CHOICES)
    brand = models.CharField(max_length=50, verbose_name="Brand Name", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Available")
    pimage = models.ImageField(upload_to='images', verbose_name="Product Image")

    def __str__(self):
        return self.name

# Cart model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

    def total_price(self):
        return self.quantity * self.product.price
    
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=255, unique=True)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Order #{self.order_id} by {self.user.username}"

class PasswordResetOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    def is_valid(self):
        from datetime import timedelta, timezone
        return self.created_at >= timezone.now() - timedelta(minutes=10)
