from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import City, Information, History
from .forms import AddCityForm


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
        # context = self.get_context_data(**kwargs)
        # print(context)
        # print(request.POST)
        return redirect("/")