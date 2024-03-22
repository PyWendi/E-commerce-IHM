from django.db import models

class Purchase(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey("authentication.CustomUser", on_delete=models.CASCADE)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.date.strftime('%Y-%m-%d %H:%M:%S')


class Order(models.Model):
    quantity = models.IntegerField()
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.purchase.date}  {self.product.name}"
