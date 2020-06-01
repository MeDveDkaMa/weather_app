from django.urls import path
from . import views

urlpatterns = [
    path('', views.CurrentTemperatureView.as_view()),
    # path('api/forecast', views.forecast),
    # path('api/test', views.get_temperature_history)
]
