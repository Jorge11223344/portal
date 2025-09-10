# portal
posrtal inmobiliario
############################################################################
Hito 1 — Conectando Django a PostgreSQL (Portal de Arriendos)
#############################################################################
Objetivo: Crear un proyecto Django conectado a PostgreSQL para un portal de arriendo de inmuebles, modelar entidades con llaves foráneas, ejecutar operaciones CRUD y documentar el proceso.



1) Instalación de entorno (3 puntos)
1.1. Instalar PostgreSQL


1.2. Crear base de datos 

1.3. Crear y activar entorno virtual



python -m venv entorno

source venv/bin/activate

1.4. Instalar dependencias
pip install para requirements.txt
django==5.2.6
psycopg[binary]==3.2.1
python-dotenv==1.0.1


psycopg[binary] es el driver para PostgreSQL.

1.5. Crear proyecto y app 
django-admin startproject proyecto .
python manage.py startapp portal


Agrega la app en pproyecto/settings.py:

INSTALLED_APPS = [
    # ...
    'portal',
]

2) Conexión a la base de datos + Modelo relacional 
2.1. Configurar PostgreSQL en proyecto/settings.py


Crea un archivo .env en la raíz del proyecto:


2.2. Modelo de datos (llaves primarias y foráneas)

class Region(models.Model):
    nro_region = models.CharField(max_length=5) #XVII
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.nombre} ||| numero de region es: {self.nro_region}"   # Valparasio ||| numero de regios es : V

class Comuna(models.Model):
    nombre = models.CharField(max_length=50)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="comunas")

    def __str__(self):
        return f"{self.nombre} ||| numero de region es: {self.region}"   # valparaiso ||| numero de region es : valparaiso
    

2.3. Migraciones y verificación
python manage.py makemigrations
python manage.py migrate


Si cambias un modelo existente (por ejemplo agregar auto_now_add=True en una tabla con datos), Django puede pedir un default para filas existentes. Acepta timezone.now o define un valor en el modelo.

3) Crud del sistema

@method_decorator(login_required, name="dispatch")
class PerfilInmuebleListView(ListView):
    model = Inmueble
    template_name = "perfil/inmueble_list.html"
    context_object_name = "inmuebles"
    paginate_by = 10
    def get_queryset(self): return Inmueble.objects.filter(propietario=self.request.user).order_by("-creado")

class PerfilInmuebleCreateView(LoginRequiredMixin, CreateView):
    model = Inmueble
    form_class = InmuebleForm
    template_name = "perfil/inmueble_form.html"
    success_url = reverse_lazy("perfil_inmueble_list")

    def form_valid(self, form):
        # ✅ Asigna ANTES del super para que quede persistido
        form.instance.propietario = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name="dispatch")
class PerfilInmuebleUpdateView(UpdateView):
    model = Inmueble
    form_class = InmuebleForm
    template_name = "perfil/inmueble_form.html"
    success_url = reverse_lazy("perfil_inmueble_list")
    def get_queryset(self): return Inmueble.objects.filter(propietario=self.request.user)

@method_decorator(login_required, name="dispatch")
class PerfilInmuebleDeleteView(DeleteView):
    model = Inmueble
    template_name = "perfil/inmueble_confirm_delete.html"
    success_url = reverse_lazy("perfil_inmueble_list")
    def get_queryset(self): return Inmueble.objects.filter(propietario=self.request.user)

4) Probar crud en consola

✅ CRUD completo (cópialo tal cual en python manage.py shell)
from django.contrib.auth import get_user_model
from portal.models import Region, Comuna, Inmueble, SolicitudArriendo
from django.utils import timezone

User = get_user_model()

# -----------------------------
# CREATE (crear registros)
# -----------------------------
# 1) Región y Comuna
bio = Region.objects.create(nro_region="VIII", nombre="Región del Biobío")
conce = Comuna.objects.create(nombre="Concepción", region=bio)

# 2) Usuarios (PerfilUser)
arrendador = User.objects.create_user(
    username="propietario1",
    password="seguro123",
    first_name="María",
    last_name="Pérez",
    email="maria@example.com",
    tipo_usuario="ARRENDADOR",  # choices del PerfilUser
    rut="11.111.111-1",
)
arrendatario = User.objects.create_user(
    username="arrenda1",
    password="seguro123",
    first_name="Juan",
    last_name="González",
    email="juan@example.com",
    tipo_usuario="ARRENDATARIO",
    rut="22.222.222-2",
)

# 3) Inmueble (propiedad en arriendo)
# ojo: precio_mensual tiene max_digits=8, decimal_places=2 → hasta 999,999.99
depto = Inmueble.objects.create(
    propietario=arrendador,
    nombre="Depto céntrico 2D1B",
    descripcion="Cerca del centro y universidad",
    m2_construidos=55,
    m2_totales=60,
    estacionamientos=1,
    habitaciones=2,
    banos=1,
    direccion="Av. Principal 123",
    precio_mensual=450000,  # se guarda como Decimal("450000")
    comuna=conce,
    tipo_de_inmueble="DEPARTAMENTO",  # usar el value del choice
)

# 4) Solicitud de arriendo
sol = SolicitudArriendo.objects.create(
    inmueble=depto,
    arrendatario=arrendatario,
    mensaje="Hola, ¿está disponible desde el próximo mes?",
    estado="P",  # PENDIENTE (value del choice)
)

print("CREADOS:", bio, conce, arrendador, arrendatario, depto, sol)

# -----------------------------
# READ (listar/consultar)
# -----------------------------
# Todas las comunas de la región
print("Comunas en Biobío:", list(bio.comunas.values_list("nombre", flat=True)))

# Inmuebles en Concepción (con relateds óptimos)
props = Inmueble.objects.select_related("comuna", "propietario").filter(comuna__nombre="Concepción")
for p in props:
    print("INMUEBLE:", p.id, p.nombre, "| Comuna:", p.comuna.nombre, "| Propietario:", p.propietario.get_full_name() or p.propietario.username)

# Solicitudes pendientes del arrendatario
pendientes = SolicitudArriendo.objects.filter(arrendatario=arrendatario, estado="P")
print("Solicitudes pendientes:", pendientes.count())

# -----------------------------
# UPDATE (actualizar)
# -----------------------------
# a) Cambiar precio del inmueble
depto.precio_mensual = 430000
depto.save()
print("Nuevo precio:", depto.precio_mensual)

# b) Aceptar la solicitud
sol.estado = "A"  # ACEPTADA
sol.actualizado = timezone.now()
sol.save()
print("Solicitud actualizada:", sol.estado)

# c) Update masivo (ejemplo): marcar en bloque todas las solicitudes P como R
SolicitudArriendo.objects.filter(estado="P").update(estado="R", actualizado=timezone.now())

# -----------------------------
# DELETE (eliminar)
# -----------------------------
# Eliminar una solicitud específica
sol_id = sol.id
sol.delete()
print("Solicitud eliminada id:", sol_id)

# Precauciones de integridad:
# - Comuna.region usa CASCADE → si borras la Región, se borran sus comunas
# - Inmueble.comuna usa PROTECT → no podrás borrar una Comuna si tiene Inmuebles
# - Inmueble.propietario usa CASCADE → si borras el usuario, se borran sus Inmuebles

# Intento de borrar comuna con inmuebles (mostrará error ProtectedError)
from django.db.models.deletion import ProtectedError
try:
    conce.delete()
except ProtectedError as e:
    print("No puedes borrar la comuna porque tiene inmuebles (PROTECT):", e)

# Borrar en orden correcto:
# 1) Eliminar inmuebles del propietario
Inmueble.objects.filter(propietario=arrendador).delete()
# 2) Ahora sí puedes borrar la comuna
conce.delete()
print("Comuna borrada OK (tras eliminar inmuebles)")

