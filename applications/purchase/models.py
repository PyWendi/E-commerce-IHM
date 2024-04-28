from django.db import models

class Purchase(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey("authentication.CustomUser", verbose_name="client_set", on_delete=models.CASCADE)
    ville = models.CharField(max_length=100, null=False, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    payement_mode = models.CharField(max_length=50, null=False, blank=True)
    account_number = models.CharField(max_length=15, null=False, blank=True)

    is_delivered = models.BooleanField(default=False)
    delivery_date = models.DateTimeField(null=True)

    class Meta:
        ordering = ["-date", "is_delivered"]

    def __str__(self):
        return self.date.strftime('%Y-%m-%d %H:%M:%S')


class Order(models.Model):
    quantity = models.IntegerField()
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.purchase.date}  {self.product.name}"
