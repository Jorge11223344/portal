


from django.urls import path, include
from .views import RegionListView, RegionCreateView, RegionUpdateView, RegionDeleteView, ComunaListView,ComunaCreateView,ComunaUpdateView,ComunaDeleteView


urlpatterns = [
    path('listar_region/',RegionListView.as_view(),  name="region_list"),
    path('crear_region/', RegionCreateView.as_view(), name="crear_region"),
    path('actualizar_region/<int:pk>/', RegionUpdateView.as_view(), name="actualizar_region"),
    path('borrar_region/<int:pk>/', RegionDeleteView.as_view(), name="borrar_region"),

    path('listar_comunas/',ComunaListView.as_view(),  name="comuna_list"),
    path('crear_comuna/', ComunaCreateView.as_view(), name="crear_comuna"),
    path('actualizar_comuna/<int:pk>/', ComunaUpdateView.as_view(), name="actualizar_comuna"),
    path('borrar_comuna/<int:pk>/', ComunaDeleteView.as_view(), name="borrar_comuna"),
]
