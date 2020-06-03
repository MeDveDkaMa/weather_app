from django.urls import path
from . import views

urlpatterns = [
    path('', views.CurrentTemperatureView.as_view(), name="current_temp"),
    path('api/add/', views.AddCityView.as_view(), name="add_city"),
    # path('api/info/<int:pk>/', views.InformationCityView.as_view(), name="information_city"),
    path('api/info/', views.InformationCityView.as_view(), name="information_city"),
    path('api/addinfo/', views.AddInformationView.as_view(), name="add_info"),
    # path('api/add/<slug:slug>/', views.AddCity.as_view(), name="add_city"),
    # path('api/forecast', views.forecast),
    # path('api/test', views.get_temperature_history)
]
