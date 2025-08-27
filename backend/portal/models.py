from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.





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
        casa = "casa", _("casa")
        depto = "departamento", _("departamento")
        parcela = "parcela", _("parcela")

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
