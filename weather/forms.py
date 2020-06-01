from django import forms
from .models import City


class AddCityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = {"name"}
