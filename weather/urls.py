from django.urls import path
from . import views

urlpatterns = [
    path('', views.CurrentTemperatureView.as_view(), name="current_temp"),
    path('api/add/', views.AddCityView.as_view(), name="add_city"),
    path('api/info/<int:pk>/', views.InformationCityView.as_view(), name="information_city"),
    path('api/history/<int:pk>/', views.HistoryCityView.as_view(), name="history_city"),
    path('api/info/update/', views.UpdateInformationView.as_view(), name="update_info"),
]
