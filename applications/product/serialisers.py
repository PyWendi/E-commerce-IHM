from rest_framework import serializers
from .models import TypeProduct, Product


class TypeProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TypeProduct
        fields = ["id", "designation"]


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.PrimaryKeyRelatedField(many=False, read_only=False)

    class Meta:
        model = Product
        fields = ["url", "id", "description", "price", "expiration_date", "type"]


class TypeAndProductSerialiser(serializers.HyperlinkedModelSerializer):
    # snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    # snippets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # snippets = SnippetSerializer(many=True)
    products = ProductSerializer(many=True)

    class Meta:
        model = TypeProduct
        fields = ["id", "designation", "product"]

