from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import (
    ClienteForm,
    ClienteRegistroForm,
    ConfiguracionEstudioForm,
    FacturaForm,
    GaleriaTrabajoForm,
    LoginForm,
    ProcedimientoForm,
    ProductoForm,
    PromocionForm,
    SolicitudCitaForm,
)
from .models import Cliente, ConfiguracionEstudio, Factura, GaleriaTrabajo, Procedimiento, Producto, Promocion


def es_admin(user):
    return user.is_authenticated and user.is_staff


def configuracion_actual():
    return ConfiguracionEstudio.objects.first() or ConfiguracionEstudio.objects.create()


class StudShinyLoginView(LoginView):
    template_name = "core/auth/login.html"
    authentication_form = LoginForm

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy("admin_dashboard")
        return reverse_lazy("cliente_dashboard")


def inicio(request):
    return render(
        request,
        "core/public/inicio.html",
        {
            "configuracion": configuracion_actual(),
            "productos": Producto.objects.filter(estado="DISPONIBLE")[:4],
            "promociones": Promocion.objects.filter(activa=True)[:3],
            "galeria": GaleriaTrabajo.objects.filter(visible=True)[:4],
            "form": SolicitudCitaForm(),
        },
    )


def catalogo(request):
    productos = Producto.objects.all()
    nombre = request.GET.get("nombre", "").strip()
    categoria = request.GET.get("categoria", "").strip()
    material = request.GET.get("material", "").strip()
    color = request.GET.get("color", "").strip()
    calibre = request.GET.get("calibre", "").strip()
    precio_min = request.GET.get("precio_min", "").strip()
    precio_max = request.GET.get("precio_max", "").strip()
    orden = request.GET.get("orden", "").strip()

    if nombre:
        productos = productos.filter(nombre__icontains=nombre)
    if categoria:
        productos = productos.filter(categoria__icontains=categoria)
    if material:
        productos = productos.filter(material__icontains=material)
    if color:
        productos = productos.filter(color__icontains=color)
    if calibre:
        productos = productos.filter(calibre__icontains=calibre)
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)
    if orden == "precio_desc":
        productos = productos.order_by("-precio")
    elif orden == "precio_asc":
        productos = productos.order_by("precio")

    return render(request, "core/public/catalogo.html", {"productos": productos})


def promociones(request):
    return render(request, "core/public/promociones.html", {"promociones": Promocion.objects.filter(activa=True)})


def beneficios(request):
    return render(request, "core/public/beneficios.html")


def contacto(request):
    form = SolicitudCitaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        cita = form.save(commit=False)
        cita.estado = "SOLICITADA"
        cita.notas_cuidados = "Solicitud creada desde la pagina publica. Confirmar disponibilidad por WhatsApp."
        cita.save()
        messages.success(request, "Solicitud registrada. El estudio confirmara la disponibilidad.")
        return redirect("contacto")
    return render(request, "core/public/contacto.html", {"form": form, "configuracion": configuracion_actual()})


def registro_cliente(request):
    form = ClienteRegistroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        cliente = form.save()
        login(request, cliente.usuario)
        messages.success(request, "Registro creado correctamente.")
        return redirect("cliente_dashboard")
    return render(request, "core/auth/registro.html", {"form": form})


@login_required
def cliente_dashboard(request):
    cliente = get_object_or_404(Cliente, usuario=request.user)
    return render(
        request,
        "core/client/dashboard.html",
        {
            "cliente": cliente,
            "procedimientos": Procedimiento.objects.filter(cliente=cliente),
            "facturas": Factura.objects.filter(cliente=cliente),
            "promociones": Promocion.objects.filter(activa=True),
            "productos": Producto.objects.filter(estado="DISPONIBLE")[:4],
            "configuracion": configuracion_actual(),
        },
    )


@login_required
def cliente_agendar(request):
    cliente = get_object_or_404(Cliente, usuario=request.user)
    form = SolicitudCitaForm(request.POST or None, initial={"nombre_cliente": cliente.nombre_completo, "telefono_cliente": cliente.telefono})
    if request.method == "POST" and form.is_valid():
        cita = form.save(commit=False)
        cita.cliente = cliente
        cita.estado = "SOLICITADA"
        cita.save()
        messages.success(request, "Tu cita fue solicitada.")
        return redirect("cliente_dashboard")
    return render(request, "core/client/agendar.html", {"form": form, "cliente": cliente})


@login_required
def cliente_factura(request, pk):
    cliente = get_object_or_404(Cliente, usuario=request.user)
    factura = get_object_or_404(Factura, pk=pk, cliente=cliente)
    return render(request, "core/client/factura.html", {"factura": factura, "cliente": cliente})


@user_passes_test(es_admin)
def admin_dashboard(request):
    hoy = timezone.localdate()
    ingresos = Factura.objects.filter(pagada=True).aggregate(total=Sum("total"))["total"] or 0
    return render(
        request,
        "core/admin/dashboard.html",
        {
            "total_productos": Producto.objects.count(),
            "total_procedimientos": Procedimiento.objects.count(),
            "total_usuarios": Cliente.objects.count(),
            "total_facturas": Factura.objects.count(),
            "ingresos": ingresos,
            "stock_bajo": Producto.objects.filter(stock__lte=5).count(),
            "productos_stock_bajo": [p for p in Producto.objects.all() if p.stock_bajo],
            "procedimientos_recientes": Procedimiento.objects.select_related("cliente", "joya_utilizada")[:5],
            "citas_hoy": Procedimiento.objects.filter(fecha_cita__date=hoy),
        },
    )


@user_passes_test(es_admin)
def reportes(request):
    procedimientos_por_tipo = Procedimiento.objects.values("tipo_perforacion").annotate(total=Count("id")).order_by("-total")[:8]
    return render(
        request,
        "core/admin/reportes.html",
        {
            "ingresos": Factura.objects.filter(pagada=True).aggregate(total=Sum("total"))["total"] or 0,
            "procedimientos_por_tipo": procedimientos_por_tipo,
            "productos_stock_bajo": [p for p in Producto.objects.all() if p.stock_bajo],
            "productos_mayor_stock": Producto.objects.order_by("-stock")[:5],
        },
    )


class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not es_admin(request.user):
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)


class ProductoListView(AdminRequiredMixin, ListView):
    model = Producto
    template_name = "core/admin/productos/list.html"
    context_object_name = "productos"


class ProductoCreateView(AdminRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "core/admin/form.html"
    success_url = reverse_lazy("producto_list")


class ProductoUpdateView(AdminRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "core/admin/form.html"
    success_url = reverse_lazy("producto_list")


class ProductoDeleteView(AdminRequiredMixin, DeleteView):
    model = Producto
    template_name = "core/admin/confirm_delete.html"
    success_url = reverse_lazy("producto_list")


class ClienteListView(AdminRequiredMixin, ListView):
    model = Cliente
    template_name = "core/admin/clientes/list.html"
    context_object_name = "clientes"


class ClienteCreateView(AdminRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "core/admin/form.html"
    success_url = reverse_lazy("cliente_list")


class ClienteUpdateView(AdminRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "core/admin/form.html"
    success_url = reverse_lazy("cliente_list")


class ClienteDeleteView(AdminRequiredMixin, DeleteView):
    model = Cliente
    template_name = "core/admin/confirm_delete.html"
    success_url = reverse_lazy("cliente_list")


class ProcedimientoListView(AdminRequiredMixin, ListView):
    model = Procedimiento
    template_name = "core/admin/procedimientos/list.html"
    context_object_name = "procedimientos"


class ProcedimientoCreateView(AdminRequiredMixin, CreateView):
    model = Procedimiento
    form_class = ProcedimientoForm
    template_name = "core/admin/form.html"
    success_url = reverse_lazy("procedimiento_list")


class ProcedimientoUpdateView(AdminRequiredMixin, UpdateView):
    model = Procedimiento
    form_class = ProcedimientoForm
    template_name = "core/admin/form.html"
    success_url = reverse_lazy("procedimiento_list")


class ProcedimientoDeleteView(AdminRequiredMixin, DeleteView):
    model = Procedimiento
    template_name = "core/admin/confirm_delete.html"
    success_url = reverse_lazy("procedimiento_list")


class PromocionListView(AdminRequiredMixin, ListView):
    model = Promocion
    template_name = "core/admin/promociones/list.html"
    context_object_name = "promociones"


class PromocionCreateView(AdminRequiredMixin, CreateView):
    model = Promocion
    form_class = PromocionForm
    template_name = "core/admin/form.html"
    success_url = reverse_lazy("promocion_list")


class PromocionUpdateView(AdminRequiredMixin, UpdateView):
    model = Promocion
    form_class = PromocionForm
    template_name = "core/admin/form.html"
    success_url = reverse_lazy("promocion_list")


class PromocionDeleteView(AdminRequiredMixin, DeleteView):
    model = Promocion
    template_name = "core/admin/confirm_delete.html"
    success_url = reverse_lazy("promocion_list")


class FacturaListView(AdminRequiredMixin, ListView):
    model = Factura
    template_name = "core/admin/facturas/list.html"
    context_object_name = "facturas"


class FacturaCreateView(AdminRequiredMixin, CreateView):
    model = Factura
    form_class = FacturaForm
    template_name = "core/admin/form.html"
    success_url = reverse_lazy("factura_list")


class FacturaUpdateView(AdminRequiredMixin, UpdateView):
    model = Factura
    form_class = FacturaForm
    template_name = "core/admin/form.html"
    success_url = reverse_lazy("factura_list")


class FacturaDeleteView(AdminRequiredMixin, DeleteView):
    model = Factura
    template_name = "core/admin/confirm_delete.html"
    success_url = reverse_lazy("factura_list")


class GaleriaListView(AdminRequiredMixin, ListView):
    model = GaleriaTrabajo
    template_name = "core/admin/galeria/list.html"
    context_object_name = "galeria"


class GaleriaCreateView(AdminRequiredMixin, CreateView):
    model = GaleriaTrabajo
    form_class = GaleriaTrabajoForm
    template_name = "core/admin/form.html"
    success_url = reverse_lazy("galeria_list")


class GaleriaUpdateView(AdminRequiredMixin, UpdateView):
    model = GaleriaTrabajo
    form_class = GaleriaTrabajoForm
    template_name = "core/admin/form.html"
    success_url = reverse_lazy("galeria_list")


class GaleriaDeleteView(AdminRequiredMixin, DeleteView):
    model = GaleriaTrabajo
    template_name = "core/admin/confirm_delete.html"
    success_url = reverse_lazy("galeria_list")


@user_passes_test(es_admin)
def configuracion(request):
    config = configuracion_actual()
    form = ConfiguracionEstudioForm(request.POST or None, instance=config)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Configuracion guardada.")
        return redirect("configuracion")
    return render(request, "core/admin/configuracion.html", {"form": form})
