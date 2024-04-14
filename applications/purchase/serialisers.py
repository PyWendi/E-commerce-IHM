from rest_framework import serializers
from applications.authentication.serialisers import UserSerializer
from applications.authentication.models import CustomUser
from applications.product.models import Product
from applications.product.serialisers import ProductSerializer
from .models import Purchase, Order


class OrderSerialiser(serializers.ModelSerializer):
    purchase = serializers.PrimaryKeyRelatedField(queryset=Purchase.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

class OrderDetailedSerialiser(serializers.ModelSerializer):
    purchase = serializers.PrimaryKeyRelatedField(queryset=Purchase.objects.all())
    product = ProductSerializer(read_only=True)

    # def create(self, validated_data):
    #     print("Inside create overrider")
    #     print(validated_data.pop("product")[0])
    #     product = Product.objects.get(pk=int(validated_data.pop("product")[0]))
    #     print(product)
    #     order = Order.objects.create(product=product, **validated_data)
    #     return order

    class Meta:
        model = Order
        fields = ["id", "purchase", "quantity", "product"]


class PurchaseSerialiser(serializers.ModelSerializer):
    client = CustomUser()
    date = serializers.DateTimeField(read_only=True)
    orders = OrderSerialiser(source="order_set", many=True, read_only=True)
    account_number = serializers.CharField(write_only=True)


    class Meta:
        model = Purchase
        fields = ["id", "date", "client", "address", "orders", "payement_mode", "account_number"]

class PurchaseWithDetailedSerialiser(serializers.ModelSerializer):
    client = CustomUser()
    date = serializers.DateTimeField(read_only=True)
    orders = OrderDetailedSerialiser(source="order_set", many=True, read_only=True)
    account_number = serializers.CharField(write_only=True)


    class Meta:
        model = Purchase
        fields = ["id", "date", "client", "address", "orders", "payement_mode", "account_number"]
