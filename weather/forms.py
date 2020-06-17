from django import forms
from django.forms import TextInput, HiddenInput

from .models import City, Information


class AddCityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = {"name"}
        widgets = {'name': TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Введите город',
                                            'style': 'width:300px'
                                            })}


class AddCityFormByID(forms.ModelForm):
    class Meta:
        model = Information
        fields = {"coord_lon", "coord_lat"}
        widgets = {'coord_lon': HiddenInput(attrs={'class': 'form-control'}),
                   'coord_lat': HiddenInput(attrs={'class': 'form-control'})
                   }
