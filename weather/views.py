from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import City, Information, History
from .forms import AddCityForm, AddInformationForm
from datetime import datetime
import requests
import time


class BaseView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["city_list"] = City.objects.all()
        context["form"] = AddCityForm
        return context


class CurrentTemperatureView(BaseView):
    template_name = 'weather/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AddCityView(BaseView):
    template_name = 'weather/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context

    def post(self, request, *args, **kwargs):
        token = 'ca8ee28f8bf42eb6948dba8bcc7aa661'
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=ru&appid=' + token

        context = super().get_context_data(**kwargs)
        form = AddCityForm(request.POST)
        if form.is_valid():
            form.save()

        info_form_data = form.cleaned_data
        context["c_info"] = info_form_data

        try:
            info_city = City.objects.get(name=info_form_data["name"])
            context["cur_info"] = info_city
            print("Найдено")
        except:
            raise Http404

        cities = City.objects.all()
        for city in cities:
            res = requests.get(url.format(city.name)).json()
            city_info = {
                'coord_lon': res["coord"]["lon"],
                'coord_lat': res["coord"]["lat"],
                'sky': res["weather"][0]["description"],
                'icon': res["weather"][0]["icon"],
                'temp': res["main"]["temp"],
                'temp_feels': res["main"]["feels_like"],
                'temp_min': res["main"]["temp_min"],
                'temp_max': res["main"]["temp_max"],
                'pressure': res["main"]["pressure"],
                'humidity': res["main"]["humidity"],
                'visibility': res["visibility"],
                'speed': res["wind"]["speed"],
                'time': datetime.utcfromtimestamp(res["dt"] + res["timezone"]).strftime('%H:%M:%S %Y-%m-%d '),
                'country': res["sys"]["country"],
                'sunrise': datetime.utcfromtimestamp(res["sys"]["sunrise"] + res["timezone"]).strftime('%H:%M:%S'),
                'sunset': datetime.utcfromtimestamp(res["sys"]["sunset"] + res["timezone"]).strftime('%H:%M:%S'),
                'city': city.name
            }

            Information.objects.update_or_create(city_id=info_city.id)
            Information.objects.filter(city_id=info_city.id).update(coord_lon=city_info['coord_lon'])
            Information.objects.filter(city_id=info_city.id).update(coord_lat=city_info['coord_lat'])
            Information.objects.filter(city_id=info_city.id).update(sky=city_info['sky'])
            Information.objects.filter(city_id=info_city.id).update(icon=city_info['icon'])
            Information.objects.filter(city_id=info_city.id).update(temperature=city_info['temp'])
            Information.objects.filter(city_id=info_city.id).update(feels_like=city_info['temp_feels'])
            Information.objects.filter(city_id=info_city.id).update(temp_min=city_info['temp_min'])
            Information.objects.filter(city_id=info_city.id).update(temp_max=city_info['temp_max'])
            Information.objects.filter(city_id=info_city.id).update(pressure=city_info['pressure'])
            Information.objects.filter(city_id=info_city.id).update(humidity=city_info['humidity'])
            Information.objects.filter(city_id=info_city.id).update(visibility=city_info['visibility'])
            Information.objects.filter(city_id=info_city.id).update(speed=city_info['speed'])
            Information.objects.filter(city_id=info_city.id).update(time=city_info['time'])
            Information.objects.filter(city_id=info_city.id).update(country=city_info['country'])
            Information.objects.filter(city_id=info_city.id).update(sunrise=city_info['sunrise'])
            Information.objects.filter(city_id=info_city.id).update(sunset=city_info['sunset'])

        return redirect("/")
        # return self.render_to_response(context)

        # return redirect("information_city" + "/" + info_city.id.__str__())


class InformationCityView(BaseView):
    template_name = 'weather/cityInformation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cur_city"] = City.objects.filter(id=kwargs["pk"])
        return context


class UpdateInformationView(BaseView):
    template_name = 'weather/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        token = 'ca8ee28f8bf42eb6948dba8bcc7aa661'
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=ru&appid=' + token

        cities = City.objects.all()
        for city in cities:
            res = requests.get(url.format(city.name)).json()
            city_info = {
                'coord_lon': res["coord"]["lon"],
                'coord_lat': res["coord"]["lat"],
                'sky': res["weather"][0]["description"],
                'icon': res["weather"][0]["icon"],
                'temp': res["main"]["temp"],
                'temp_feels': res["main"]["feels_like"],
                'temp_min': res["main"]["temp_min"],
                'temp_max': res["main"]["temp_max"],
                'pressure': res["main"]["pressure"],
                'humidity': res["main"]["humidity"],
                'visibility': res["visibility"],
                'speed': res["wind"]["speed"],
                'time': datetime.utcfromtimestamp(res["dt"] + res["timezone"]).strftime('%H:%M:%S %Y-%m-%d '),
                'country': res["sys"]["country"],
                'sunrise': datetime.utcfromtimestamp(res["sys"]["sunrise"] + res["timezone"]).strftime('%H:%M:%S'),
                'sunset': datetime.utcfromtimestamp(res["sys"]["sunset"] + res["timezone"]).strftime('%H:%M:%S'),
                'city': city.name,
            }
            print("API RESPONSE:", city_info)

            Information.objects.filter(city_id=city.id).update(coord_lon=city_info['coord_lon'])
            Information.objects.filter(city_id=city.id).update(coord_lat=city_info['coord_lat'])
            Information.objects.filter(city_id=city.id).update(sky=city_info['sky'])
            Information.objects.filter(city_id=city.id).update(icon=city_info['icon'])
            Information.objects.filter(city_id=city.id).update(temperature=city_info['temp'])
            Information.objects.filter(city_id=city.id).update(feels_like=city_info['temp_feels'])
            Information.objects.filter(city_id=city.id).update(temp_min=city_info['temp_min'])
            Information.objects.filter(city_id=city.id).update(temp_max=city_info['temp_max'])
            Information.objects.filter(city_id=city.id).update(pressure=city_info['pressure'])
            Information.objects.filter(city_id=city.id).update(humidity=city_info['humidity'])
            Information.objects.filter(city_id=city.id).update(visibility=city_info['visibility'])
            Information.objects.filter(city_id=city.id).update(speed=city_info['speed'])
            Information.objects.filter(city_id=city.id).update(time=city_info['time'])
            Information.objects.filter(city_id=city.id).update(country=city_info['country'])
            Information.objects.filter(city_id=city.id).update(sunrise=city_info['sunrise'])
            Information.objects.filter(city_id=city.id).update(sunset=city_info['sunset'])
        return redirect("/")


class AllCityTemperatureView(BaseView):
    template_name = 'charts/allTemperature.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CityTemperatureHistory(BaseView):
    template_name = 'charts/historyTemperature.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        token = 'ca8ee28f8bf42eb6948dba8bcc7aa661'
        url = 'http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={}&lon={}&dt={}&units=metric&appid=' + token

        lat = Information.objects.get(city_id=kwargs["pk"]).coord_lat
        lon = Information.objects.get(city_id=kwargs["pk"]).coord_lon
        # Current unix time - 1 day
        dt = int(time.time()) + 360 - 86400
        res = requests.get(url.format(lat, lon, dt)).json()
        city_name = City.objects.get(id=kwargs["pk"])
        context["city"] = city_name

        all_history = []
        for i in range(0, 24):
            history_info = {
                'time': datetime.utcfromtimestamp(res["hourly"][i]["dt"] +
                                                  res["timezone_offset"]).strftime('%Y-%m-%d %H:%M '),
                'temp': res["hourly"][i]["temp"],
            }
            all_history.append(history_info)

        context["history_context"] = all_history

        print(context["history_context"])

        return context
