from django.db import models
from django.conf import settings  

# Create your models here.
class Branch(models.Model):

    name = models.CharField(max_length=100)
    location = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)


class Employee(models.Model):

    ROLE_CHOICES = [
        ("waiter", "Waiter"),
        ("bartender", "Bartender"),
        ("meat_staff", "Meat staff"),
        ("cashier", "Cashier"),
        ("manager", "Manager"),
    ]
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Product(models.Model):
    CATEGORY = [("beverage", "Beverage"), ("meat", "Meat")]
    name = models.CharField(max_length=100)
    product_category = models.CharField(max_length=20, choices=CATEGORY)
    unit = models.CharField(max_length=20)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

class CustomerOrder(models.Model):  
    STATUS = [("pending", "Pending"), ("completed", "Completed"), ("cancelled", "Cancelled")]
    order_number = models.CharField(max_length=50, unique=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # Fixed reference to Employee
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=20, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class OrderItem(models.Model):  
    STATUS = [
        ("queued", "Queued"),
        ("ready", "Ready"),
        ("rejected", "Rejected"),
    ]
    order = models.ForeignKey(CustomerOrder, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    item_status = models.CharField(max_length=20, choices=STATUS, default="queued")
