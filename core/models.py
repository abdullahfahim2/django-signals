from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.stock})"


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate total price before saving
        if self.product and self.quantity:
            self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale of {self.product.name} - {self.quantity}"
    
class ActivityLog(models.Model):
    action = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

