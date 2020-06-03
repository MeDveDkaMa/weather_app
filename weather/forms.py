from django import forms
from .models import City, Information


class AddCityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = {"name"}


class AddInformationForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = {"temperature", "coord_lat", "coord_lon", "sky"}
