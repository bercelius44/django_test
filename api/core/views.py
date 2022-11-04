from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import math

from core import serializers
from core.models import Order, DriverRecord


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

        order = Order.objects.filter(driver = driver)

        def check_time_range(item):
            """Function to check if order time is out of previus range time."""
            high_time_decimal = (int(item.time.split(':')[0]) + 1)* 3600 + int(item.time.split(':')[1]) * 60
            low_time_decimal = (int(item.time.split(':')[0]) - 1)* 3600 + int(item.time.split(':')[1]) * 60
            time_decimal = int(time.split(':')[0]) * 3600 + int(time.split(':')[1]) * 60

            return high_time_decimal >= time_decimal >= low_time_decimal

        for item in order.iterator():  
            if item.date == date and check_time_range(item):
                return Response({'message': 'An order is already scheduled for the driver in the same time.'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order(date=date, time=time, pick_up_place=pick_up_place, delivery_place=delivery_place, driver=driver)
        order.save()
        
        return Response({'message': 'Order created'})


class GetOrdersByDay(APIView):
    """Endpoint to get all orders in a specific day."""  
    serializer_class = serializers.OrdersByDaySerializer        

    def get(self, request, format = None):
        """Return the list of all orders for a specific day."""  
        serializers = self.serializer_class(data = request.data)

        if not serializers.is_valid():
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)  

        date = serializers.validated_data.get('date')        
        orders = Order.objects.filter(date=date)
        day_orders = []

        for item in orders.iterator():
            day_orders.append([item.time, item.date.strftime("%d-%m-%Y"), item.pick_up_place, item.delivery_place, item.driver])

        day_orders.sort()

        day_orders_dic = []
        for order in day_orders:
            day_orders_dic.append({'date': order[1],
                                'time': order[0],
                                'pick_up_place': order[2],
                                'delivery_place': order[3],
                                'driver': order[4]})            

        return Response({'orders': day_orders_dic})
        

class GetOrdersByDriver(APIView):
    """Endpoint to get all orders for one driver in a specific day."""
    serializer_class = serializers.OrdersByDriverSerializer

    def get(self, request, format = None):
        """Return the list of all orders for a driver in a specific day."""
        serializers = self.serializer_class(data = request.data)

        if not serializers.is_valid():
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

        date = serializers.validated_data.get('date') 
        driver = serializers.validated_data.get('driver')     
        orders = Order.objects.filter(date = date, driver = driver)

        day_orders = []

        for item in orders.iterator():
            day_orders.append([item.time, item.date.strftime("%d-%m-%Y"), item.pick_up_place, item.delivery_place, item.driver])

        day_orders.sort()

        day_orders_dic = []
        for order in day_orders:
            day_orders_dic.append({'date': order[1],
                                'time': order[0],
                                'pick_up_place': order[2],
                                'delivery_place': order[3],
                                'driver': order[4]})            

        return Response({'driver_orders': day_orders_dic})


class GetClosestDriver(APIView):
    """Endpoint to get the closest driver to a certain point."""
    serializer_class = serializers.ClosestDriverSerializer

    def get(self, request, format = None):
        """Return the closest driver to a certain point acording to his availability."""
        serializers = self.serializer_class(data = request.data)

        if not serializers.is_valid():
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

        date = serializers.validated_data.get('date')
        time = serializers.validated_data.get('time')
        location = serializers.validated_data.get('location')

        drivers = DriverRecord.objects.all()
        orders = Order.objects.filter(date=date)
        availableDrivers = [item.pk for item in drivers.iterator()]

        def check_time_range(item):
            """Function to check if order time is out of previus range time."""
            high_time_decimal = (int(item.time.split(':')[0]) + 1)* 3600 + int(item.time.split(':')[1]) * 60
            low_time_decimal = (int(item.time.split(':')[0]) - 1)* 3600 + int(item.time.split(':')[1]) * 60
            time_decimal = int(time.split(':')[0]) * 3600 + int(time.split(':')[1]) * 60

            return high_time_decimal >= time_decimal >= low_time_decimal

        for item in orders.iterator():  
            if item.date == date and check_time_range(item):
                availableDrivers.remove(item.driver)
        
        x1 = int(location.split(',')[0])
        y1 = int(location.split(',')[1])
        min_distance = 150
        driver = 0

        for item in drivers.iterator():
            x2 = int(item.location.split(',')[0])
            y2 = int(item.location.split(',')[1])

            distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
                        
            if distance < min_distance:     
                if item.pk in availableDrivers:
                    min_distance = distance
                    driver = item.pk

        return Response({'closest_driver': driver})
        
            