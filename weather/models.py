from django.db import models


class City(models.Model):
    name = models.CharField("Имя", max_length=30)

    def __str__(self):
        return self.name


class Information(models.Model):
    city = models.OneToOneField(City, on_delete=models.CASCADE, null=True)
    temperature = models.CharField("Температура", max_length=5, null=True)
    icon = models.CharField("Иконка", max_length=5, null=True)
    coord_lon = models.CharField("Долгота", max_length=5, null=True)
    coord_lat = models.CharField("Широта", max_length=5, null=True)
    sky = models.CharField("Облачность", max_length=5, null=True)
    pressure = models.CharField("Давление", max_length=5, null=True)
    humidity = models.CharField("Влажность", max_length=5, null=True)
    temp_min = models.CharField("Минимальная температура", max_length=5, null=True)
    temp_max = models.CharField("Максимальная температура", max_length=5, null=True)
    speed = models.CharField("Скорость ветра", max_length=5, null=True)
    country = models.CharField("Страна", max_length=5, null=True)
    feels_like = models.CharField("Чувствуется как", max_length=5, null=True)
    time = models.CharField("Время", max_length=5, null=True)
    sunrise = models.CharField("Восход", max_length=5, null=True)
    sunset = models.CharField("Закат", max_length=5, null=True)
