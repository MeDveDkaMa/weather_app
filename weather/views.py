from django.shortcuts import render
from django.views.generic import TemplateView
from .models import City, Information, History


class CurrentTemperatureView(TemplateView):
    template_name = 'weather/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["information"] = Information.objects.all()
        context["city"] = City.objects.all()
        return context
