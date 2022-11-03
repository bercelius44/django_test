from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core import serializers


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
        message = f'Data: {date}, {time}, {pick_up_place}, {delivery_place}, {driver}'
        
        return Response({'message': message})
        
            