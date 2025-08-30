from django.shortcuts import render
from .models import (
    Region,
    Comuna,
    Inmueble
)
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)


from .form import (
    RegionForm,
    ComunaForm
)

from django.urls import reverse, reverse_lazy
# Create your views here.


#CRUD para region
class RegionListView(ListView):
    model = Region
    template_name = "inmuebles/region_list.html"
    context_object_name = "regiones"

class RegionCreateView(CreateView):
    model = Region
    form_class = RegionForm
    template_name = "inmuebles/region_form.html"
    success_url = reverse_lazy("region_list")  # redirecciona al nombre de la direccion

class RegionUpdateView(UpdateView):  
    model = Region
    form_class = RegionForm
    template_name = "inmuebles/region_form.html"
    success_url = reverse_lazy("region_list")  # 



class RegionDeleteView(DeleteView):
    model = Region
    template_name= "inmuebles/region_confirm.html"
    success_url = reverse_lazy("region_list")


###################################################################
# CRUD para comuna
####################################################################

class ComunaListView(ListView):
    model = Comuna
    template_name = "inmuebles/comuna_list.html"
    context_object_name = "comunas"

class ComunaCreateView(CreateView):
    model = Comuna
    form_class = ComunaForm
    template_name = "inmuebles/comuna_form.html"
    success_url = reverse_lazy("comuna_list")  # redirecciona al nombre de la direccion


class ComunaUpdateView(UpdateView):
    model = Comuna
    form_class = ComunaForm
    template_name = "inmuebles/comuna_form.html"
    success_url = reverse_lazy("comuna_list") 

class ComunaDeleteView(DeleteView):
    model = Comuna
    template_name= "inmuebles/comuna_delete.html"
    success_url = reverse_lazy("comuna_list")


#####################################################################

#CRUD para Inmueble
###################################################################333

