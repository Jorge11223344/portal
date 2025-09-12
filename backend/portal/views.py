from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin  # ✅ agregado
from django.views.generic import ListView, CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy

from .models import Inmueble, SolicitudArriendo, Comuna, Region
from .form import RegisterForm, LoginForm, PerfilUserForm, SolicitudArriendoForm


# HOME: lista de inmuebles (con filtros por región y comuna)
class HomeInmuebleListView(ListView):
    model = Inmueble
    template_name = "web/home.html"
    context_object_name = "inmuebles"
    paginate_by = 12
    ordering = ["-creado"]

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related("comuna", "comuna__region")
            .order_by("-creado")
        )
        comuna_id = self.request.GET.get("comuna")
        region_id = self.request.GET.get("region")

        if comuna_id:
            qs = qs.filter(comuna_id=comuna_id)
        if region_id:
            qs = qs.filter(comuna__region_id=region_id)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # data para selects
        ctx["comunas"] = Comuna.objects.all().order_by("nombre")
        ctx["regiones"] = Region.objects.all().order_by("nombre")
        # valores seleccionados (para mantener selección en el template)
        ctx["selected_comuna"] = self.request.GET.get("comuna", "")
        ctx["selected_region"] = self.request.GET.get("region", "")
        # para preservar filtros en la paginación
        qd = self.request.GET.copy()
        if "page" in qd:
            del qd["page"]
        ctx["querystring"] = qd.urlencode()
        return ctx


# AUTH
def register_view(request):
    if request.method == "POST":
        # ✅ incluir archivos por 'imagen'
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Cuenta creada correctamente.")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

@ensure_csrf_cookie      # asegura cookie en el GET
@csrf_protect            # protege el POST
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


# PERFIL (muestra enviadas/recibidas y datos del usuario)
class PerfilView(LoginRequiredMixin, TemplateView):  # ✅ protegido con login
    template_name = "usuarios/perfil.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        u = self.request.user
        ctx["usuario"] = u
        ctx["enviadas"] = (
            u.solicitudes_enviadas
            .select_related("inmueble", "inmueble__comuna")
            .order_by("-creado")
        )
        ctx["recibidas"] = (
            SolicitudArriendo.objects
            .filter(inmueble__propietario=u)
            .select_related("inmueble", "inmueble__comuna", "arrendatario")
            .order_by("-creado")
        )
        return ctx


class PerfilEditView(LoginRequiredMixin, UpdateView):
    form_class = PerfilUserForm
    template_name = "usuarios/perfil_edit.html"
    success_url = reverse_lazy("perfil")

    def get_object(self, queryset=None):
        # Edita siempre el usuario logueado
        return self.request.user

    def form_valid(self, form):
        form.save()  # guarda efectivamente
        messages.success(self.request, "Perfil actualizado correctamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Verás los errores en los logs del contenedor
        print("❌ PerfilEditView.form_invalid ->", form.errors)
        messages.error(self.request, "Revisa los campos marcados en rojo.")
        return super().form_invalid(form)


# CREAR SOLICITUD (muestra datos del inmueble)
class SolicitudArriendoCreateView(LoginRequiredMixin, CreateView):  # ✅ exige login
    model = SolicitudArriendo
    form_class = SolicitudArriendoForm
    template_name = "inmuebles/solicitud_form.html"
    success_url = reverse_lazy("perfil")

    def dispatch(self, request, *args, **kwargs):
        self.inmueble = get_object_or_404(Inmueble, pk=kwargs["inmueble_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["inmueble"] = self.inmueble
        return ctx

    def form_valid(self, form):
        # (Opcional pero recomendado) Solo arrendatarios pueden enviar solicitudes
        if self.request.user.tipo_usuario != "ARRENDATARIO":
            messages.error(self.request, "Solo los arrendatarios pueden enviar solicitudes.")
            return redirect("home")

        solicitud = form.save(commit=False)
        solicitud.inmueble = self.inmueble
        solicitud.arrendatario = self.request.user
        solicitud.save()
        messages.success(self.request, "¡Solicitud enviada con éxito!")
        return redirect(self.success_url)


def _redir(request, fallback="perfil"):
    return request.POST.get("next") or request.META.get("HTTP_REFERER") or reverse_lazy(fallback)


@login_required
@require_POST
def solicitud_aceptar(request, pk: int):
    s = get_object_or_404(SolicitudArriendo, pk=pk, inmueble__propietario=request.user)
    if s.estado != s.EstadoSolicitud.ACEPTADA:
        s.estado = s.EstadoSolicitud.ACEPTADA
        s.save(update_fields=["estado", "actualizado"])
        messages.success(request, "Solicitud aceptada.")
    else:
        messages.info(request, "La solicitud ya estaba aceptada.")
    return redirect(_redir(request))


@login_required
@require_POST
def solicitud_rechazar(request, pk: int):
    s = get_object_or_404(SolicitudArriendo, pk=pk, inmueble__propietario=request.user)
    if s.estado != s.EstadoSolicitud.RECHAZADA:
        s.estado = s.EstadoSolicitud.RECHAZADA
        s.save(update_fields=["estado", "actualizado"])
        messages.warning(request, "Solicitud rechazada.")
    else:
        messages.info(request, "La solicitud ya estaba rechazada.")
    return redirect(_redir(request))
