from django.shortcuts import render
from .models import (
    Region
)
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView
)


from .form import (
    RegionForm
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







