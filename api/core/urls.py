from core.drivers_location.drivers_location_updater import update_drivers_location
from django.urls import path

from core import views


urlpatterns = [
     path('create_order/', views.ScheduleOrderView.as_view(), name = 'create_order'),
     path('day_orders/<str:date>/', views.GetOrdersByDayView.as_view(), name = 'day_orders'),
     path('driver_orders/<str:date>/<int:driver>', views.GetOrdersByDriverView.as_view(), name = 'driver_orders'),
     path('closest_driver/<str:date>/<str:time>/<str:location>', views.GetClosestDriverView.as_view(), name = 'closest_driver'),
]

update_drivers_location()
