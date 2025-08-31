


from django.urls import path, include
from .views import * 


urlpatterns = [
    path('listar_region/',RegionListView.as_view(),  name="region_list"),
    path('crear_region/', RegionCreateView.as_view(), name="crear_region"),
    path('actualizar_region/<int:pk>/', RegionUpdateView.as_view(), name="actualizar_region"),
    path('borrar_region/<int:pk>/', RegionDeleteView.as_view(), name="borrar_region"),

    path('listar_comunas/',ComunaListView.as_view(),  name="comuna_list"),
    path('crear_comuna/', ComunaCreateView.as_view(), name="crear_comuna"),
    path('actualizar_comuna/<int:pk>/', ComunaUpdateView.as_view(), name="actualizar_comuna"),
    path('borrar_comuna/<int:pk>/', ComunaDeleteView.as_view(), name="borrar_comuna"),

    path('listar_inmuebles/',InmuebleListView.as_view(),  name="inmueble_list"),
    path('crear_inmueble/', InmuebleCreateView.as_view(), name="crear_inmueble"),
    path('actualizar_inmueble/<int:pk>/', InmuebleUpdateView.as_view(), name="actualizar_inmueble"),
    path('borrar_inmueble/<int:pk>/', InmuebleDeleteView.as_view(), name="borrar_inmueble"),

    path('listar_solicitudes/',SolicitudArriendoListView.as_view(),  name="solicitud_list"),
    path('crear_solicitud/', SolicitudArriendoCreateView.as_view(), name="crear_solicitud"),
    path('actualizar_solicitud/<int:pk>/', SolicitudArriendoUpdateView.as_view(), name="actualizar_solicitud"),
    path('borrar_solicitud/<int:pk>/', SolicitudArriendoDeleteView.as_view(), name="borrar_solicitud"),

    path('actualizar_perfil/<int:pk>/', PerfilUserUpdateView.as_view(), name="actualizar_perfil"),
    

]
