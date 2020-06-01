from django.urls import path
from . import views

urlpatterns = [
    path('', views.CurrentTemperatureView.as_view(), name="current_temp"),
    path('api/add/', views.AddCity.as_view(), name="add_city"),
    # path('api/forecast', views.forecast),
    # path('api/test', views.get_temperature_history)
]
