from django.urls import path

from core import views


urlpatterns = [
     path('', views.AboutApiView.as_view()),
     path('create_order/', views.ScheduleApiView.as_view()),
]