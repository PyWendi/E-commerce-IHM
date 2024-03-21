from rest_framework import serializers
from applications.authentication.models import CustomUser
from .models import Purchase

class PurchaseSerialiser(serializers.ModelSerializer):
    client = CustomUser()
    class Meta:
        model = Purchase
        fields = ["date", "client"]