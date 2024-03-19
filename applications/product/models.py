from django.db import models
from datetime import datetime, timedelta

class TypeProduct(models.Model):
    designation = models.CharField(max_length=50, blank=True, default="")

    def __str__(self):
        return self.designation

def expiration():
    return datetime.now() + timedelta(days=4*365)

class Product(models.Model):
    name = models.CharField(max_length=50, blank=True, default="")
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    expiration_date = models.DateTimeField(default=expiration)
    type = models.ForeignKey(TypeProduct, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


