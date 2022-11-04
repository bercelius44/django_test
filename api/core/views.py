from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core import serializers
from core.models import Order


class AboutApiView(APIView):
    """About the API"""

    def get(self, request, format = None):
        """Return a list of the API features"""
        features = [
            'Agendar un pedido a un conductor en una fecha y hora, y especificar su lugar de recogida (latitud y longitud) y destino.',
            'Consultar todos los pedidos asignados en un día en específico ordenados por la hora.',
            'Consultar todos los pedidos de un conductor en un día en específico ordenados por la hora.',
            'Hacer búsquedas del conductor que esté más cerca de un punto geográfico en una fecha y hora.'
        ]

        return Response({'message':'About', 'features': features})


class ScheduleApiView(APIView):
    """Endpoint to schedule a delivery"""
    serializer_class = serializers.OrderSerializer

    def post(self, request):
        """Create a delivery order in the system."""
        serializers = self.serializer_class(data = request.data)

        if not serializers.is_valid():
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

        date = serializers.validated_data.get('date')
        time = serializers.validated_data.get('time')
        pick_up_place = serializers.validated_data.get('pick_up_place')
        delivery_place = serializers.validated_data.get('delivery_place')
        driver = serializers.validated_data.get('driver')       

        # order = Order(pk=driver, date=date, time=time, pick_up_place=pick_up_place,  
        #                 delivery_place=delivery_place, driver=driver)

        # order.save()
        order = Order.objects.get(pk=driver)
        order.pick_up_place = pick_up_place
        order.save()

        message = f'Data: {date}, {time}, {pick_up_place}, {delivery_place}, {driver}'
        
        return Response({'message': message})


class GetOrdersByDay(APIView):
    """Endpoint to get all orders in a specific day."""

    def get(self, request, format = None):
        """Return the list of all orders for a specific day."""
        orders = Order.objects.all()

        return Response({'message': orders})
        

class GetOrdersByDriver(APIView):
    """Endpoint to get all orders for one driver in a specific day."""

    def get(self, request, format = None):
        """Return the list of all orders for a driver in a specific day."""
        orders = Order.objects.all()

        return Response({'message': orders})


class GetClosestDriver(APIView):
    """Endpoint to get the closest driver to a certain point."""

    def get(self, request, format = None):
        """Return the closest driver to a certain point acording to his availability."""
        orders = Order.objects.all()

        return Response({'message': orders})
        
            