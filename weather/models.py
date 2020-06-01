from django.db import models


class City(models.Model):
    name = models.CharField("Имя", max_length=10)

    def __str__(self):
        return self.name


class Information(models.Model):
    city = models.OneToOneField(City, on_delete=models.CASCADE, null=True)
    temperature = models.CharField("Температура", max_length=5, null=True)
    icon = models.CharField("Иконка", max_length=5, null=True)
    coord_lon = models.CharField("Долгота", max_length=5, null=True)
    coord_lat = models.CharField("Широта", max_length=5, null=True)
    sky = models.CharField("Облачность", max_length=5, null=True)


class Forecast(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.CharField("Температура", max_length=5)
    time = models.CharField("Время", max_length=15)


class History(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.CharField("Температура", max_length=5)
    time = models.CharField("Время", max_length=15)
# Create your models here.
