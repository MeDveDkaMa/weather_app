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

    def post(self, request, *args, **kwargs):
        form = AddCityForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("information_city")


class InformationCityView(BaseView):
    template_name = 'weather/cityInformation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


class AddInformationView(BaseView):
    template_name = 'weather/index.html'

    def post(self, request, *args, **kwargs):
        form = AddInformationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("information_city")
