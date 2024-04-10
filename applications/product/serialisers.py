from rest_framework import serializers
from .models import TypeProduct, Product, Rating


class TypeProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TypeProduct
        fields = ["id", "designation"]


class ProductSerializer(serializers.ModelSerializer):
    # type = serializers.PrimaryKeyRelatedField()
    image = serializers.ImageField(allow_empty_file=False, allow_null=True)
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "rate", "expiration_date", "type", "image", "stock"]


class ProductImageUpdateSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["image"]

class RateSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "rate_value"]


class TypeAndProductSerialiser(serializers.HyperlinkedModelSerializer):
    # snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    # snippets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # snippets = SnippetSerializer(many=True)
    products = ProductSerializer(source="product_set", many=True)

    class Meta:
        model = TypeProduct
        fields = ["id", "designation", "products"]


