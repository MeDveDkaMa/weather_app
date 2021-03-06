from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView
from .models import City, Information
from .forms import AddCityForm, AddCityFormByID
from datetime import datetime
import requests
import time


class BaseView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["city_list"] = City.objects.all()
        context["form"] = AddCityForm
        context["formCoord"] = AddCityFormByID
        return context


class CurrentTemperatureView(BaseView):
    template_name = 'weather/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AddCityByNameView(BaseView):
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
            form.save(commit=False)
        else:
            redirect("/")

        info_form_data = form.cleaned_data

        try:
            info_city = City.objects.create(name=info_form_data["name"])
        except:
            raise Http404

        cities = City.objects.all()
        for city in cities:
            res = requests.get(url.format(city.name)).json()
            if res["cod"] == "404" or not ('country' in res["sys"]):
                City.objects.get(name=info_form_data["name"]).delete()
                redirect("current_temp")
                break

            city_info = {
                'coord_lon': res["coord"]["lon"],
                'coord_lat': res["coord"]["lat"],
                'sky': res["weather"][0]["description"],
                'icon': res["weather"][0]["icon"],
                'temp': res["main"]["temp"],
                'temp_feels': res["main"]["feels_like"],
                'temp_min': res["main"]["temp_min"],
                'temp_max': res["main"]["temp_max"],
                'pressure': res["main"]["pressure"] // 1.333224,
                'humidity': res["main"]["humidity"],
                'speed': res["wind"]["speed"],
                'time': datetime.utcfromtimestamp(time.time() + res["timezone"]).strftime('%H:%M:%S %Y-%m-%d '),
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
            Information.objects.filter(city_id=info_city.id).update(speed=city_info['speed'])
            Information.objects.filter(city_id=info_city.id).update(time=city_info['time'])
            Information.objects.filter(city_id=info_city.id).update(country=city_info['country'])
            Information.objects.filter(city_id=info_city.id).update(sunrise=city_info['sunrise'])
            Information.objects.filter(city_id=info_city.id).update(sunset=city_info['sunset'])

        return redirect("/")


class AddCityByCoordView(BaseView):
    template_name = 'weather/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):

        token = 'ca8ee28f8bf42eb6948dba8bcc7aa661'
        url = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&lang=ru&units=metric&appid=' + token
        url2 = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=ru&appid=' + token

        context = super().get_context_data(**kwargs)
        form = AddCityFormByID(request.POST)
        if form.is_valid():
            form.save(commit=False)
        else:
            redirect("/")

        res_coord = requests.get(url.format(request.POST['coord_lat'], request.POST['coord_lon'])).json()

        if res_coord["cod"] == "400" or not ("name" in res_coord) or (res_coord["name"] == ""):
            return redirect("current_temp")

        try:
            info_city = City.objects.create(name=res_coord["name"])
        except:
            raise Http404

        cities = City.objects.all()
        for city in cities:
            res = requests.get(url2.format(city.name)).json()
            if res["cod"] == "404":
                City.objects.get(name=res_coord["name"]).delete()
                redirect("current_temp")
                break

            city_info = {
                'coord_lon': res["coord"]["lon"],
                'coord_lat': res["coord"]["lat"],
                'sky': res["weather"][0]["description"],
                'icon': res["weather"][0]["icon"],
                'temp': res["main"]["temp"],
                'temp_feels': res["main"]["feels_like"],
                'temp_min': res["main"]["temp_min"],
                'temp_max': res["main"]["temp_max"],
                'pressure': res["main"]["pressure"] // 1.333224,
                'humidity': res["main"]["humidity"],
                'speed': res["wind"]["speed"],
                'time': datetime.utcfromtimestamp(time.time() + res["timezone"]).strftime('%H:%M:%S %Y-%m-%d '),
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
            Information.objects.filter(city_id=info_city.id).update(speed=city_info['speed'])
            Information.objects.filter(city_id=info_city.id).update(time=city_info['time'])
            Information.objects.filter(city_id=info_city.id).update(country=city_info['country'])
            Information.objects.filter(city_id=info_city.id).update(sunrise=city_info['sunrise'])
            Information.objects.filter(city_id=info_city.id).update(sunset=city_info['sunset'])

        return redirect("/")


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
                'pressure': res["main"]["pressure"] // 1.333224,
                'humidity': res["main"]["humidity"],
                'speed': res["wind"]["speed"],
                'time': datetime.utcfromtimestamp(time.time() + res["timezone"]).strftime('%H:%M:%S %Y-%m-%d '),
                'country': res["sys"]["country"],
                'sunrise': datetime.utcfromtimestamp(res["sys"]["sunrise"] + res["timezone"]).strftime('%H:%M:%S'),
                'sunset': datetime.utcfromtimestamp(res["sys"]["sunset"] + res["timezone"]).strftime('%H:%M:%S'),
                'city': city.name,
            }

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
            Information.objects.filter(city_id=city.id).update(speed=city_info['speed'])
            Information.objects.filter(city_id=city.id).update(time=city_info['time'])
            Information.objects.filter(city_id=city.id).update(country=city_info['country'])
            Information.objects.filter(city_id=city.id).update(sunrise=city_info['sunrise'])
            Information.objects.filter(city_id=city.id).update(sunset=city_info['sunset'])
        return redirect("/")


class DeleteCityView(BaseView):
    template_name = 'weather/cityInformation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        City.objects.get(id=kwargs["pk"]).delete()
        return redirect("/")


class AllCityTemperatureView(BaseView):
    template_name = 'charts/allTemperature.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CityHistoryView(BaseView):
    template_name = 'charts/historyInformation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        token = 'ca8ee28f8bf42eb6948dba8bcc7aa661'
        url = 'http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={}&lon={}&dt={}&units=metric&lang=ru&appid=' + token

        lat = Information.objects.get(city_id=kwargs["pk"]).coord_lat
        lon = Information.objects.get(city_id=kwargs["pk"]).coord_lon

        all_history = []

        if kwargs["type"] == 1:
            # Current unix time - 1 day
            dt = int(time.time()) + 360 - kwargs["time"]
            res = requests.get(url.format(lat, lon, dt)).json()
            city_name = City.objects.get(id=kwargs["pk"])
            context["city"] = city_name

            for i in range(0, 24):
                history_info = {
                    'time': datetime.utcfromtimestamp(res["hourly"][i]["dt"] +
                                                      res["timezone_offset"]).strftime('%Y-%m-%d %H:%M '),
                    'temp': res["hourly"][i]["temp"],
                }
                all_history.append(history_info)

            context["history_context"] = all_history
            print(context["history_context"])

        if kwargs["type"] == 2:
            while kwargs["time"] >= 86400:
                # Current unix time - 1 day
                dt = int(time.time()) + 360 - kwargs["time"]
                res = requests.get(url.format(lat, lon, dt)).json()
                city_name = City.objects.get(id=kwargs["pk"])
                context["city"] = city_name

                for i in range(0, 24):
                    history_info = {
                        'time': datetime.utcfromtimestamp(res["hourly"][i]["dt"] +
                                                          res["timezone_offset"]).strftime('%Y-%m-%d %H:%M '),
                        'temp': res["hourly"][i]["temp"],
                    }
                    all_history.append(history_info)
                kwargs["time"] -= 86400
            context["history_context"] = all_history
        return context


class CityForecastView(BaseView):
    template_name = 'charts/forecastInformation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        token = 'ca8ee28f8bf42eb6948dba8bcc7aa661'
        url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&lang=ru&units=metric&appid=' + token

        lat = Information.objects.get(city_id=kwargs["pk"]).coord_lat
        lon = Information.objects.get(city_id=kwargs["pk"]).coord_lon
        # response daily + hourly
        type_request = "current"

        res = requests.get(url.format(lat, lon, type_request)).json()

        city_name = City.objects.get(id=kwargs["pk"])
        context["city"] = city_name

        all_forecast = []

        for i in range(0, kwargs["count"]):
            forecast_info = {
                'time': datetime.utcfromtimestamp(res[kwargs["type"]][i]["dt"] +
                                                  res["timezone_offset"]).strftime('%m-%d %H:%M '),
                'pressure': res[kwargs["type"]][i]['pressure'] // 1.333224,
                'info': res[kwargs["type"]][i],
            }
            all_forecast.append(forecast_info)

        context["forecast_context"] = all_forecast
        context["type"] = kwargs["type"]

        print(context["forecast_context"])

        return context
