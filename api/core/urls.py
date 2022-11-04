from core.drivers_location.drivers_location_updater import update_drivers_location
from django.urls import path

from core import views


urlpatterns = [
     path('', views.AboutApiView.as_view()),
     path('create_order/', views.ScheduleApiView.as_view()),
     path('day_orders/', views.GetOrdersByDay.as_view()),
     path('driver_orders/', views.GetOrdersByDriver.as_view()),
     path('closest_driver/', views.GetClosestDriver.as_view()),
]

update_drivers_location()
