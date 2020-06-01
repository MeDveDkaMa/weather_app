from django.contrib import admin
from weather.models import City,Forecast,Information

# Register your models here.
admin.site.register(City)
admin.site.register(Forecast)
admin.site.register(Information)
