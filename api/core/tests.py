from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

VALID_DATE = '2022-11-04'
INVALID_DATE = 'yyyy-mm-dd'
VALID_TIME = '12:00'
INVALID_TIME = 'HH:MM'
VALID_LOCATION = '50,50'
INVALID_LOCATION = 'A,A'
DRIVER = 1


class GetOrdersByDayTest(APITestCase):
    """Test the GetOrdersByDayTest endpoint."""
    def test_invalid_date(self):
        """Tests an invalid date."""
        response = self.client.get(reverse('day_orders', kwargs={'date':INVALID_DATE}))       
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'date': ['Date has wrong format. Use one of these formats instead: YYYY-MM-DD.']})
    
    def test_valid_date(self):
        """Tests a valid date."""
        response = self.client.get(reverse('day_orders', kwargs={'date':VALID_DATE}))       
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'orders': []})


class GetOrdersByDriverTest(APITestCase):
    """Test the GetOrdersByDriver endpoint."""
    def test_invalid_date(self):
        """Tests an invalid date"""
        response = self.client.get(reverse('driver_orders', kwargs={'date':INVALID_DATE, 'driver':DRIVER}))               
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'date': ['Date has wrong format. Use one of these formats instead: YYYY-MM-DD.']})
    
    def test_valid_date(self):
        """Tests an invalid driver"""
        response = self.client.get(reverse('driver_orders', kwargs={'date':VALID_DATE, 'driver': DRIVER}))      
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'driver_orders': []})


class GetClosestDriverTest(APITestCase):
    """Test the GetClosestDriver endpoint."""
    def test_invalid_date(self):
        """Test an invalid date."""
        response = self.client.get(reverse('closest_driver', kwargs={'date':INVALID_DATE, 
                                                                    'time':VALID_TIME, 
                                                                    'location':VALID_LOCATION}))       
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'date': ['Date has wrong format. Use one of these formats instead: YYYY-MM-DD.']})
    
    def test_invalid_time(self):
        """Test an invalid time."""
        response = self.client.get(reverse('closest_driver', kwargs={'date':VALID_DATE, 
                                                                    'time':INVALID_TIME, 
                                                                    'location':VALID_LOCATION})) 
           
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'time': ['HH:MM is not in a valid format (HH:MM).']})
    
    def test_invalid_location(self):
        """Test an invalid location"""
        response = self.client.get(reverse('closest_driver', kwargs={'date':VALID_DATE, 
                                                                    'time':VALID_TIME, 
                                                                    'location':INVALID_LOCATION}))       
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'location': ['A,A is not in a valid format (0,0 to 100,100)']})
        
    def test_valid_request(self):
        """Test a valid request"""
        response = self.client.get(reverse('closest_driver', kwargs={'date':VALID_DATE, 
                                                                    'time':VALID_TIME, 
                                                                    'location':VALID_LOCATION}))  
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'closest_driver': 14})


class ScheduleOrderTest(APITestCase):
    """Test the ScheduleOrder endpoint."""
    def test_invalid_date(self):
        """Test an invalid date."""
        response = self.client.post(reverse('create_order'), data={'date': INVALID_DATE, 
                                                                    'time': VALID_TIME,
                                                                    'pick_up_place': VALID_LOCATION,
                                                                    'delivery_place': VALID_LOCATION,
                                                                    'driver': DRIVER})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'date': ['Date has wrong format. Use one of these formats instead: YYYY-MM-DD.']})
    
    def test_invalid_time(self):
        """Test an invalid time."""
        response = self.client.post(reverse('create_order'), data={'date': VALID_DATE, 
                                                                    'time': INVALID_TIME,
                                                                    'pick_up_place': VALID_LOCATION,
                                                                    'delivery_place': VALID_LOCATION,
                                                                    'driver': DRIVER})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'time': ['HH:MM is not in a valid format (HH:MM).']})
    
    def test_invalid_pick_up_place(self):
        """Test an invalid pick up place."""
        response = self.client.post(reverse('create_order'), data={'date': VALID_DATE, 
                                                                    'time': VALID_TIME,
                                                                    'pick_up_place': INVALID_LOCATION,
                                                                    'delivery_place': VALID_LOCATION,
                                                                    'driver': DRIVER})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'pick_up_place': ['A,A is not in a valid format (0,0 to 100,100)']})
    
    def test_invalid_delivary_place(self):
        """Test an invalid delivery place."""
        response = self.client.post(reverse('create_order'), data={'date': VALID_DATE, 
                                                                    'time': VALID_TIME,
                                                                    'pick_up_place': VALID_LOCATION,
                                                                    'delivery_place': INVALID_LOCATION,
                                                                    'driver': DRIVER})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'delivery_place': ['A,A is not in a valid format (0,0 to 100,100)']})

    def test_invalid_driver(self):
        """Test an invalid driver."""
        response = self.client.post(reverse('create_order'), data={'date': VALID_DATE, 
                                                                    'time': VALID_TIME,
                                                                    'pick_up_place': VALID_LOCATION,
                                                                    'delivery_place': VALID_LOCATION,
                                                                    'driver': 'DRIVER'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'driver': ['A valid integer is required.']})

    def test_valid_order(self):
        """Test a valid oder"""
        response = self.client.post(reverse('create_order'), data={'date': VALID_DATE, 
                                                                    'time': VALID_TIME,
                                                                    'pick_up_place': VALID_LOCATION,
                                                                    'delivery_place': VALID_LOCATION,
                                                                    'driver': DRIVER})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'Order created'})
