from rest_framework import serializers
from .models import Product, Order, MeasurementData, Payment


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class MeasurementDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementData
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
