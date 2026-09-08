from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from decimal import Decimal, InvalidOperation

from .models import Cliente, ConfiguracionEstudio, Factura, GaleriaTrabajo, Procedimiento, Producto, Promocion


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Correo electronico", widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Contrasena", widget=forms.PasswordInput(attrs={"class": "form-control"}))


class ClienteRegistroForm(forms.ModelForm):
    password = forms.CharField(label="Contrasena", widget=forms.PasswordInput)

    class Meta:
        model = Cliente
        fields = [
            "nombre_completo",
            "tipo_documento",
            "numero_documento",
            "edad",
            "tipo_sangre",
            "correo",
            "telefono",
            "contacto_emergencia",
            "tipo_perforacion_interes",
            "alergias_patologias",
            "numero_perforaciones",
        ]

    def clean_correo(self):
        correo = self.cleaned_data["correo"].lower()
        if User.objects.filter(username=correo).exists() or Cliente.objects.filter(correo=correo).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo.")
        return correo

    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.correo = self.cleaned_data["correo"].lower()
        user = User.objects.create_user(
            username=cliente.correo,
            email=cliente.correo,
            password=self.cleaned_data["password"],
            first_name=cliente.nombre_completo,
            is_staff=False,
        )
        cliente.usuario = user
        if commit:
            cliente.save()
        return cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            "nombre_completo",
            "tipo_documento",
            "numero_documento",
            "edad",
            "tipo_sangre",
            "correo",
            "telefono",
            "contacto_emergencia",
            "tipo_perforacion_interes",
            "alergias_patologias",
            "numero_perforaciones",
        ]


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "nombre",
            "categoria",
            "material",
            "color",
            "calibre",
            "medida",
            "precio",
            "stock",
            "stock_minimo",
            "descripcion",
            "imagen",
            "en_promocion",
        ]


class ProcedimientoForm(forms.ModelForm):
    fecha_cita = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))

    class Meta:
        model = Procedimiento
        fields = [
            "cliente",
            "nombre_cliente",
            "telefono_cliente",
            "tipo_perforacion",
            "fecha_cita",
            "estado",
            "estado_pago",
            "notas_cuidados",
            "joya_utilizada",
            "materiales_medicos",
        ]


class SolicitudCitaForm(forms.ModelForm):
    fecha_cita = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))

    class Meta:
        model = Procedimiento
        fields = ["nombre_cliente", "telefono_cliente", "tipo_perforacion", "fecha_cita"]


class PromocionForm(forms.ModelForm):
    class Meta:
        model = Promocion
        fields = ["nombre", "descripcion", "precio", "activa"]


class FacturaForm(forms.ModelForm):
    total = forms.CharField(
        label="Total",
        widget=forms.TextInput(
            attrs={
                "inputmode": "decimal",
                "placeholder": "Ejemplo: 100.000 o 100.000,50",
            }
        ),
    )

    class Meta:
        model = Factura
        fields = ["cliente", "procedimiento", "total", "metodo_pago", "pagada"]

    def clean_total(self):
        valor = self.cleaned_data["total"].strip().replace("$", "").replace(" ", "")

        if "," in valor:
            # Formato colombiano: 100.000,50
            valor = valor.replace(".", "").replace(",", ".")
        elif valor.count(".") > 1 or (
            "." in valor and len(valor.rsplit(".", 1)[1]) == 3
        ):
            # Puntos usados como separadores de miles: 100.000
            valor = valor.replace(".", "")

        try:
            total = Decimal(valor)
        except InvalidOperation:
            raise forms.ValidationError("Ingrese un total válido, por ejemplo 100.000 o 100.000,50.")

        if total < 1:
            raise forms.ValidationError("El total debe ser mayor o igual a 1.")
        if total.as_tuple().exponent < -2:
            raise forms.ValidationError("El total puede tener máximo 2 decimales.")
        if total >= Decimal("100000000"):
            raise forms.ValidationError("El total es demasiado grande.")

        return total


class GaleriaTrabajoForm(forms.ModelForm):
    class Meta:
        model = GaleriaTrabajo
        fields = ["titulo", "descripcion", "imagen", "visible"]


class ConfiguracionEstudioForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionEstudio
        fields = ["nombre", "direccion", "telefono", "correo", "horario", "mensaje_cuidados"]
