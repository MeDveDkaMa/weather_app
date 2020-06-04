from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import City, Information, History
from .forms import AddCityForm, AddInformationForm
import requests


class BaseView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["information_list"] = Information.objects.all()
        context["city_list"] = City.objects.all()
        context["form"] = AddCityForm
        context["info_form"] = AddInformationForm
        return context


class CurrentTemperatureView(BaseView):
    template_name = 'weather/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


class AddCityView(BaseView):
    template_name = 'weather/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context

    def post(self, request, *args, **kwargs):
        token = 'ca8ee28f8bf42eb6948dba8bcc7aa661'
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + token

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
                'city': city.name,
                'temp': res["main"]["temp"],
                'icon': res["weather"][0]["icon"],
                'sky': res["weather"][0]["description"],
                'coord_lon': res["coord"]["lon"],
                'coord_lat': res["coord"]["lat"],
            }

            Information.objects.update_or_create(city_id=info_city.id)
            Information.objects.filter(city_id=info_city.id).update(temperature=city_info['temp'])
            Information.objects.filter(city_id=info_city.id).update(coord_lon=city_info['coord_lon'])
            Information.objects.filter(city_id=info_city.id).update(coord_lat=city_info['coord_lat'])
            Information.objects.filter(city_id=info_city.id).update(sky=city_info['sky'])
            Information.objects.filter(city_id=info_city.id).update(icon=city_info['icon'])
        return redirect("/")
        # return self.render_to_response(context)

        # return redirect("information_city" + "/" + info_city.id.__str__())


class InformationCityView(BaseView):
    template_name = 'weather/cityInformation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


class HistoryCityView(BaseView):
    template_name = 'charts/hTemperature.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


class UpdateInformationView(BaseView):
    template_name = 'weather/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
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
            print("API RESPONSE:", city_info)
            Information.objects.filter(city_id=city.id).update(temperature=city_info['temp'])
            Information.objects.filter(city_id=city.id).update(coord_lon=city_info['coord_lon'])
            Information.objects.filter(city_id=city.id).update(coord_lat=city_info['coord_lat'])
            Information.objects.filter(city_id=city.id).update(sky=city_info['sky'])
            Information.objects.filter(city_id=city.id).update(icon=city_info['icon'])

        return redirect("/")


class AllCityTemperatureView(BaseView):
    template_name = 'charts/cTemperature.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CityTemperatureHistory(TemplateView):
    template_name = 'charts/hTemperature.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = City.objects.all()
        return context
