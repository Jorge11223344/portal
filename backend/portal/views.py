
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
    PerfilUserForm,
    RegisterForm
)

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from .form import RegisterForm, LoginForm
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_protect


# Create your views here.

def home(request):
    return render(request,"web/home.html")




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


#CRUD solicitu de arriendo
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
    template_name = "inmuebles/inmueble_form.html"  ###revisar el form si esta bien puesto
    success_url = reverse_lazy("solicitud_list") 

class SolicitudArriendoDeleteView(DeleteView):
    model = SolicitudArriendo
    template_name= "inmuebles/solicitud_confirm.html"
    success_url = reverse_lazy("solicitud_list")  


######################################################
#CRUD PerfilUser
#####################################################

class PerfilUserUpdateView(UpdateView):
    model = PerfilUser
    form_class = PerfilUserForm
    template_name = "usuarios/perfil_form.html"
    success_url = reverse_lazy("solicitud_list") 



#login/logout/register
###################################################################
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Cuenta creada correctamente.")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, "Has iniciado sesión.")
        return redirect("home")
    return render(request, "registration/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión.")
    return redirect("login")