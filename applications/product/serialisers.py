from rest_framework import serializers
from .models import TypeProduct, Product


class TypeProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TypeProduct
        fields = ["id", "designation"]


class ProductSerializer(serializers.ModelSerializer):
    # type = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "expiration_date", "type"]


class TypeAndProductSerialiser(serializers.HyperlinkedModelSerializer):
    # snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    # snippets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # snippets = SnippetSerializer(many=True)
    products = ProductSerializer(source="product_set", many=True)

    class Meta:
        model = TypeProduct
        fields = ["id", "designation", "products"]

