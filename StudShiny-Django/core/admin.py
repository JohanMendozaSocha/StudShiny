from django.contrib import admin

from .models import Cliente, ConfiguracionEstudio, Factura, GaleriaTrabajo, Procedimiento, Producto, Promocion


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre_completo", "correo", "telefono", "tipo_documento", "numero_documento")
    search_fields = ("nombre_completo", "correo", "numero_documento")


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "material", "precio", "stock", "stock_minimo", "estado")
    list_filter = ("categoria", "material", "estado", "en_promocion")
    search_fields = ("nombre", "categoria", "material")


@admin.register(Procedimiento)
class ProcedimientoAdmin(admin.ModelAdmin):
    list_display = ("nombre_cliente", "tipo_perforacion", "fecha_cita", "estado", "estado_pago")
    list_filter = ("estado", "estado_pago", "tipo_perforacion")
    search_fields = ("nombre_cliente", "telefono_cliente", "tipo_perforacion")


admin.site.register(Promocion)
admin.site.register(Factura)
admin.site.register(GaleriaTrabajo)
admin.site.register(ConfiguracionEstudio)
