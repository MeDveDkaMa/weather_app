from django import forms
from django.forms import TextInput

from .models import City


class AddCityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = {"name"}
        widgets = {'name': TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Введите город',
                                            'style': 'width:300px'
                                            })}
