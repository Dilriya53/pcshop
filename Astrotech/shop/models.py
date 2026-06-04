from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    """Product model for ASTRO TECH components"""
    CATEGORY_CHOICES = [
        ('cpu', 'CPU'),
        ('gpu', 'GPU'),
        ('motherboard', 'Motherboard'),
        ('ram', 'RAM'),
        ('storage', 'Storage'),
        ('psu', 'Power Supply'),
        ('case', 'Case'),
        ('cooling', 'Cooling'),
        ('accessories', 'Accessories'),
        ('pc', 'Gaming PC'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='products_created')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
