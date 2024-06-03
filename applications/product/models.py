from django.db import models
from datetime import datetime, timedelta


def expiration():
    return datetime.now() + timedelta(days=4*365)


def upload_to(instance, filename):
    """

    @param filename:
    @type instance: object
    """
    return 'product_images/' + filename


class TypeProduct(models.Model):
    designation = models.CharField(max_length=50, blank=True, default="")

    class Meta:
        ordering = ["designation"]

    def __str__(self):
        return self.designation


class Product(models.Model):
    name = models.CharField(max_length=50, blank=True, default="")
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    rate = models.IntegerField(default=0, null=True)
    expiration_date = models.DateTimeField(default=expiration, null=True)
    type = models.ForeignKey(TypeProduct, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Rating(models.Model):
    rate_value = models.IntegerField(default=0)
    user_id = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name
