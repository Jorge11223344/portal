


from django.urls import path, include
from .views import RegionListView, RegionCreateView, RegionUpdateView


urlpatterns = [
    path('listar_region/',RegionListView.as_view(),  name="region_list"),
    path('crear_region/', RegionCreateView.as_view(), name="crear_region"),
    path('actualizar_region/<int:pk>/', RegionUpdateView.as_view(), name="actualizar_region"),
]
