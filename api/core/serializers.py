from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    """Serializes an order request object."""
    date = serializers.DateField()
    time = serializers.CharField(max_length = 5)
    pick_up_place = serializers.CharField(max_length = 7)
    delivery_place = serializers.CharField(max_length = 7)
    driver = serializers.IntegerField()