from rest_framework import serializers
from .models import Product, Order

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'pk',
            'name',
            'description',
            'discount',
            'created_at',
            'archived',
            'preview'
        )

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'pk',
            'user',
            'delivery_address',
            'promocode',
            'created_at',
            'products',
            'receipt'
        )
