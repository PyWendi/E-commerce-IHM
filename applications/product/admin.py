from django.contrib import admin
from .models import TypeProduct, Product, Rating

# Register your models here.
admin.site.register(TypeProduct)
admin.site.register(Product)
admin.site.register(Rating)