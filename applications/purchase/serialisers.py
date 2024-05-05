from rest_framework import serializers
from applications.authentication.models import CustomUser
from applications.product.models import Product
from applications.product.serialisers import ProductSerializer
from .models import Purchase, Order


class OrderSerialiser(serializers.ModelSerializer):
    purchase = serializers.PrimaryKeyRelatedField(queryset=Purchase.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Order
        fields = "__all__"

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
        fields = "__all__"


class PurchaseSerialiser(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    orders = OrderSerialiser(source="order_set", many=True, read_only=True)
    account_number = serializers.CharField(write_only=True, required=False)
    ville = serializers.CharField(required=False)
    pays = serializers.CharField(required=False)

    class Meta:
        model = Purchase
        fields = "__all__"

class PurchaseForUpdateSerialiser(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    account_number = serializers.CharField(read_only=True, required=False)
    ville = serializers.CharField(required=False)
    pays = serializers.CharField(required=False)

    class Meta:
        model = Purchase
        fields = "__all__"

class PurchaseSimpleDataSerialiser(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    account_number = serializers.CharField(write_only=True)
    ville = serializers.CharField(required=False)
    pays = serializers.CharField(required=False)

    class Meta:
        model = Purchase
        fields = "__all__"

class PurchaseWithDetailedSerialiser(serializers.ModelSerializer):
    client = CustomUser()
    date = serializers.DateTimeField(read_only=True)
    orders = OrderDetailedSerialiser(source="order_set", many=True, read_only=True)
    account_number = serializers.CharField(write_only=True)
    ville = serializers.CharField(required=False)
    pays = serializers.CharField(required=False)


    class Meta:
        model = Purchase
        fields = "__all__"

class PurchaseForUserSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Purchase
        fields = ["id", "address", "ville", "date", "payement_mode", "is_delivered", "delivery_date"]

