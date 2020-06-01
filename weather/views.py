from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import City, Information, History
from .forms import AddCityForm
import requests


class BaseView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["information_list"] = Information.objects.all()
        context["city_list"] = City.objects.all()
        context["form"] = AddCityForm
        return context


class CurrentTemperatureView(BaseView):
    template_name = 'weather/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["information_list"] = Information.objects.all()
        # context["city_list"] = City.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        print(context)

        return self.render_to_response(context)


class AddCity(BaseView):

    def post(self, request, *args, **kwargs):

        form = AddCityForm(request.POST)
        if form.is_valid():
            print("valid")
            form.save()


        token = 'ca8ee28f8bf42eb6948dba8bcc7aa661'
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + token

        cities = City.objects.all()
        for city in cities:
            res = requests.get(url.format(city.name)).json()
            city_info = {
                'city': city.name,
                'temp': res["main"]["temp"],
                'icon': res["weather"][0]["icon"],
                'sky': res["weather"][0]["description"],
                'coord_lon': res["coord"]["lon"],
                'coord_lat': res["coord"]["lat"],
            }

            Information.objects.filter(city__name=city_info['city']).update(temperature=city_info['temp'])
            Information.objects.filter(city__name=city_info['city']).update(sky=city_info['sky'])
            Information.objects.filter(city__name=city_info['city']).update(coord_lon=city_info['coord_lon'])
            Information.objects.filter(city__name=city_info['city']).update(coord_lat=city_info['coord_lat'])

        # context = self.get_context_data(**kwargs)
        # print(context)
        print(request.POST)
        return redirect("/")
