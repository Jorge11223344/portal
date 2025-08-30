from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid
from django.contrib.auth.models import AbstractUser
from django.conf import settings



class Region(models.Model):
    nro_region=models.CharField(max_length=5) 
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.nombre} ||| numero de region es : {self.nro_region}"  #Valparaiso  ||| numero de region es : V

class Comuna(models.Model):
    nombre = models.CharField(max_length=50)
    region=models.ForeignKey(Region, on_delete=models.CASCADE, related_name="comunas")

    def __str__(self):
        return f"{self.nombre} ||| numero de region es : {self.region}"  #Valparaiso  ||| numero de region es : V


#modelo de inmueble 
class Inmueble(models.Model):
    class Tipo_de_inmueble(models.TextChoices):
        casa = "CASA", _("Casa")
        depto = "DEPARTAMENTO", _("Departamento")
        parcela = "PARCELA", _("Parcela")

    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inmuebles", blank=True, null=True)

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    m2_construidos = models.FloatField(default=0)
    m2_totales = models.FloatField(default=0)
    estacionamientos = models.PositiveSmallIntegerField(default=0)
    habitaciones = models.PositiveSmallIntegerField(default=0)
    banos = models.PositiveSmallIntegerField(default=0)
    direccion = models.CharField(max_length=100)
    precio_mensual = models.DecimalField(max_digits=8,decimal_places=2)
    creado = models.DateTimeField(auto_now_add=True)
    actuallizado= models.DateTimeField(auto_now=True)
    comuna=models.ForeignKey(Comuna, on_delete=models.PROTECT, related_name="inmuebles")
    #tipo de inmueble
    tipo_de_inmueble = models.CharField(max_length=20, choices=Tipo_de_inmueble.choices)


    def __str__(self):
        return f"propietario = {self.propietario}  nombre: {self.nombre} "  
    
class SolicitudArriendo(models.Model):
    class EstadoSolicitud(models.TextChoices):
        pendiente = "P", _("Pendiente")
        aceptada = "A", _("Aceptada")
        rechazada = "R", _("Rechazada")


    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name="solicitudes")
    arrendatario= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="solicitudes_enviadas")
    mensaje = models.TextField()
    estado = models.CharField(max_length=10, choices=EstadoSolicitud.choices, default=EstadoSolicitud.pendiente)
    creado = models.DateTimeField(auto_now_add=True)
    actuallizado= models.DateTimeField(auto_now=True)


    def __str__(self):
        return f" {self.uuid}  nombre: {self.inmueble} {self.estado}"  
    

class PerfilUser(AbstractUser):

       
    class TipoUsuario(models.TextChoices):
        ARRENDATARIO = "ARRENDATARIO", _("Pendiente")
        ARRENDADOR = "ARRENDADOR", _("Arrendador")
        
    
    tipo_usuario = models.CharField(max_length=13, choices=TipoUsuario.choices, default=TipoUsuario.ARRENDATARIO)
    rut = models.CharField(max_length=50, unique=True, blank=True, null=True)

    

    def __str__(self):
        return f" {self.get_full_name()}  | {self.tipo_usuario} "  
    

