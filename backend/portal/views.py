from django.shortcuts import render
from .models import (
    Region,
    Comuna,
    Inmueble,
    SolicitudArriendo,
    PerfilUser
)
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)


from .form import (
    RegionForm,
    ComunaForm,
    InmuebleForm,
    SolicitudArriendoForm,
    PerfilUserForm
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

class InmuebleListView(ListView):
    model = Inmueble
    template_name = "inmuebles/inmueble_list.html"
    context_object_name = "inmuebles"


class InmuebleCreateView(CreateView):
    model = Inmueble
    form_class = InmuebleForm
    template_name = "inmuebles/inmueble_form.html"
    success_url = reverse_lazy("inmueble_list")  # redirecciona al nombre de la direccion

class InmuebleUpdateView(UpdateView):
    model = Inmueble
    form_class = InmuebleForm
    template_name = "inmuebles/inmueble_form.html"
    success_url = reverse_lazy("inmueble_list")   

class InmuebleDeleteView(DeleteView):
    model = Inmueble
    template_name= "inmuebles/inmueble_confirm.html"
    success_url = reverse_lazy("inmueble_list")

################################################################################



################################################################################3

class SolicitudArriendoListView(ListView):
    model = SolicitudArriendo
    template_name = "inmuebles/solicitudes_list.html"
    context_object_name = "solicitudes"

class SolicitudArriendoCreateView(CreateView):
    model = SolicitudArriendo
    form_class = SolicitudArriendoForm
    template_name = "inmuebles/solicitud_form.html"
    success_url = reverse_lazy("solicitud_list")  # redirecciona al nombre de la direccion

class SolicitudArriendoUpdateView(UpdateView):
    model = SolicitudArriendo
    form_class = SolicitudArriendoForm
    template_name = "inmuebles/inmueble_form.html"
    success_url = reverse_lazy("solicitud_list") 

class SolicitudArriendoDeleteView(DeleteView):
    model = SolicitudArriendo
    template_name= "inmuebles/solicitud_confirm.html"
    success_url = reverse_lazy("solicitud_list")  


######################################################

#####################################################

class PerfilUserUpdateView(UpdateView):
    model = PerfilUser
    form_class = PerfilUserForm
    template_name = "inmuebles/inmueble_form.html"
    success_url = reverse_lazy("solicitud_list") 

class PerfilUserDeleteView(UpdateView):
    model = PerfilUser
    form_class = PerfilUserForm
    template_name = "inmuebles/inmueble_form.html"
    success_url = reverse_lazy("solicitud_list") 