from rest_framework import serializers, viewsets
from .models import Product, CustomerOrder, OrderItem
from decimal import Decimal

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product; fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem; fields = "__all__"

class CustomerOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = CustomerOrder; fields = "__all__"

    def create(self, validated):
        items_data = validated.pop("items")
        order = CustomerOrder.objects.create(**validated)
        total = 0
        for item in items_data:
            item["order"] = order
            OrderItem.objects.create(**item)
            total += item["subtotal"]
        order.total_amount = total * Decimal("1.10")  # 10 % service charge
        order.save()
        return order

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

class CustomerOrderViewSet(viewsets.ModelViewSet):
    queryset = CustomerOrder.objects.all()
    serializer_class = CustomerOrderSerializer