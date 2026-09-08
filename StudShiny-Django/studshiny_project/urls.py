from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from core import views


urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("catalogo/", views.catalogo, name="catalogo"),
    path("promociones/", views.promociones, name="promociones"),
    path("beneficios/", views.beneficios, name="beneficios"),
    path("contacto/", views.contacto, name="contacto"),
    path("registro/", views.registro_cliente, name="registro"),
    path("login/", views.StudShinyLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="inicio"), name="logout"),
    path("cliente/dashboard/", views.cliente_dashboard, name="cliente_dashboard"),
    path("cliente/agendar/", views.cliente_agendar, name="cliente_agendar"),
    path("cliente/factura/<int:pk>/", views.cliente_factura, name="cliente_factura"),
    path("panel/", views.admin_dashboard, name="admin_dashboard"),
    path("panel/reportes/", views.reportes, name="reportes"),
    path("panel/configuracion/", views.configuracion, name="configuracion"),
    path("panel/productos/", views.ProductoListView.as_view(), name="producto_list"),
    path("panel/productos/nuevo/", views.ProductoCreateView.as_view(), name="producto_create"),
    path("panel/productos/<int:pk>/editar/", views.ProductoUpdateView.as_view(), name="producto_update"),
    path("panel/productos/<int:pk>/eliminar/", views.ProductoDeleteView.as_view(), name="producto_delete"),
    path("panel/clientes/", views.ClienteListView.as_view(), name="cliente_list"),
    path("panel/clientes/nuevo/", views.ClienteCreateView.as_view(), name="cliente_create"),
    path("panel/clientes/<int:pk>/editar/", views.ClienteUpdateView.as_view(), name="cliente_update"),
    path("panel/clientes/<int:pk>/eliminar/", views.ClienteDeleteView.as_view(), name="cliente_delete"),
    path("panel/procedimientos/", views.ProcedimientoListView.as_view(), name="procedimiento_list"),
    path("panel/procedimientos/nuevo/", views.ProcedimientoCreateView.as_view(), name="procedimiento_create"),
    path("panel/procedimientos/<int:pk>/editar/", views.ProcedimientoUpdateView.as_view(), name="procedimiento_update"),
    path("panel/procedimientos/<int:pk>/eliminar/", views.ProcedimientoDeleteView.as_view(), name="procedimiento_delete"),
    path("panel/promociones/", views.PromocionListView.as_view(), name="promocion_list"),
    path("panel/promociones/nuevo/", views.PromocionCreateView.as_view(), name="promocion_create"),
    path("panel/promociones/<int:pk>/editar/", views.PromocionUpdateView.as_view(), name="promocion_update"),
    path("panel/promociones/<int:pk>/eliminar/", views.PromocionDeleteView.as_view(), name="promocion_delete"),
    path("panel/facturas/", views.FacturaListView.as_view(), name="factura_list"),
    path("panel/facturas/nuevo/", views.FacturaCreateView.as_view(), name="factura_create"),
    path("panel/facturas/<int:pk>/editar/", views.FacturaUpdateView.as_view(), name="factura_update"),
    path("panel/facturas/<int:pk>/eliminar/", views.FacturaDeleteView.as_view(), name="factura_delete"),
    path("panel/galeria/", views.GaleriaListView.as_view(), name="galeria_list"),
    path("panel/galeria/nuevo/", views.GaleriaCreateView.as_view(), name="galeria_create"),
    path("panel/galeria/<int:pk>/editar/", views.GaleriaUpdateView.as_view(), name="galeria_update"),
    path("panel/galeria/<int:pk>/eliminar/", views.GaleriaDeleteView.as_view(), name="galeria_delete"),
    path("django-admin/", admin.site.urls),
]
