from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Cliente(models.Model):
    TIPOS_DOCUMENTO = [
        ("Cedula de ciudadania", "Cedula de ciudadania"),
        ("Permiso especial de permanencia", "Permiso especial de permanencia"),
        ("Pasaporte", "Pasaporte"),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre_completo = models.CharField(max_length=140)
    tipo_documento = models.CharField(max_length=60, choices=TIPOS_DOCUMENTO)
    numero_documento = models.CharField(max_length=40, unique=True)
    edad = models.PositiveIntegerField(validators=[MinValueValidator(14)])
    tipo_sangre = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=30)
    contacto_emergencia = models.CharField(max_length=120, blank=True)
    tipo_perforacion_interes = models.CharField(max_length=80, blank=True)
    alergias_patologias = models.TextField(blank=True)
    numero_perforaciones = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre_completo"]

    def __str__(self):
        return self.nombre_completo


class Producto(models.Model):
    ESTADOS = [
        ("DISPONIBLE", "Disponible"),
        ("AGOTADO", "Agotado"),
    ]

    nombre = models.CharField(max_length=120)
    categoria = models.CharField(max_length=60)
    material = models.CharField(max_length=60)
    color = models.CharField(max_length=40)
    calibre = models.CharField(max_length=40, blank=True)
    medida = models.CharField(max_length=40, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=5)
    descripcion = models.TextField(blank=True)
    imagen = models.CharField(max_length=255, blank=True)
    en_promocion = models.BooleanField(default=False)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="DISPONIBLE")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["categoria", "nombre"]

    def save(self, *args, **kwargs):
        self.estado = "DISPONIBLE" if self.stock > 0 else "AGOTADO"
        super().save(*args, **kwargs)

    @property
    def stock_bajo(self):
        return self.stock <= self.stock_minimo

    def get_absolute_url(self):
        return reverse("producto_detalle", args=[self.pk])

    def __str__(self):
        return self.nombre


class Promocion(models.Model):
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["precio"]

    def __str__(self):
        return self.nombre


class Procedimiento(models.Model):
    ESTADOS = [
        ("SOLICITADA", "Solicitada"),
        ("CONFIRMADA", "Confirmada"),
        ("COMPLETADA", "Completada"),
        ("CANCELADA", "Cancelada"),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_cliente = models.CharField(max_length=140)
    telefono_cliente = models.CharField(max_length=30, blank=True)
    tipo_perforacion = models.CharField(max_length=100)
    fecha_cita = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default="SOLICITADA")
    estado_pago = models.BooleanField(default=False)
    notas_cuidados = models.TextField(blank=True)
    joya_utilizada = models.ForeignKey(
        Producto, on_delete=models.SET_NULL, null=True, blank=True, related_name="procedimientos"
    )
    materiales_medicos = models.ManyToManyField(Producto, blank=True, related_name="procedimientos_insumo")

    class Meta:
        ordering = ["-fecha_cita"]

    def save(self, *args, **kwargs):
        if self.cliente:
            self.nombre_cliente = self.cliente.nombre_completo
            self.telefono_cliente = self.cliente.telefono
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_cliente} - {self.tipo_perforacion}"


class Factura(models.Model):
    METODOS_PAGO = [
        ("PSE", "PSE"),
        ("Efectivo", "Efectivo"),
        ("Tarjeta", "Tarjeta"),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    procedimiento = models.ForeignKey(Procedimiento, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    fecha = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=40, choices=METODOS_PAGO, default="PSE")
    pagada = models.BooleanField(default=False)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"Factura #{self.id} - {self.total}"


class GaleriaTrabajo(models.Model):
    titulo = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    imagen = models.CharField(max_length=255)
    visible = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado"]

    def __str__(self):
        return self.titulo


class ConfiguracionEstudio(models.Model):
    nombre = models.CharField(max_length=120, default="StudShiny")
    direccion = models.CharField(max_length=160, default="Bogota, Colombia", blank=True)
    telefono = models.CharField(max_length=40, default="+57 302 764 10 35", blank=True)
    correo = models.EmailField(default="contacto@studshiny.com", blank=True)
    horario = models.CharField(max_length=160, default="Lunes a sabado, 10:00 a.m. a 7:00 p.m.", blank=True)
    mensaje_cuidados = models.TextField(
        default="Lava la zona con solucion salina, evita tocar la perforacion y consulta al estudio ante molestias."
    )

    def __str__(self):
        return self.nombre
