from django.urls import path
from . import views

urlpatterns = [
    path('', views.CurrentTemperatureView.as_view(), name="current_temp"),
    path('api/add/city/name', views.AddCityByNameView.as_view(), name="add_city"),
    path('api/add/city/coord', views.AddCityByCoordView.as_view(), name="add_city_by_coord"),
    path('api/info/<int:pk>/', views.InformationCityView.as_view(), name="information_city"),
    path('api/history/<int:pk>/time/<int:time>/', views.CityTemperatureHistoryView.as_view(), name="history_city"),
    path('api/info/update/', views.UpdateInformationView.as_view(), name="update_info"),
    path('api/info/temperature/all', views.AllCityTemperatureView.as_view(), name="all_temperature_info"),
    path('api/api/delete/<int:pk>/', views.DeleteCityView.as_view(), name="delete_city"),
    path('api/forecast/<int:pk>/time/<int:count>/type/<slug:type>/', views.CityForecastView.as_view(),
         name="forecast_city"),
]
