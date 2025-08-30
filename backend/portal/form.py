
from django import forms
from .models import *

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ["nro_region","nombre"]


class ComunaForm(forms.ModelForm):
    class Meta:
        model = Comuna
        fields = ["region","nombre"]

