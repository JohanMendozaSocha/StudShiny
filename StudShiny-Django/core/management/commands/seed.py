from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Cliente, ConfiguracionEstudio, Factura, GaleriaTrabajo, Procedimiento, Producto, Promocion


class Command(BaseCommand):
    help = "Carga datos iniciales para StudShiny en Django."

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(
            username="admin@studshiny.com",
            defaults={"email": "admin@studshiny.com", "first_name": "Administradora StudShiny", "is_staff": True, "is_superuser": True},
        )
        admin.set_password("1234")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

        empleado, _ = User.objects.get_or_create(
            username="empleado@studshiny.com",
            defaults={"email": "empleado@studshiny.com", "first_name": "Empleado StudShiny", "is_staff": True},
        )
        empleado.set_password("1234")
        empleado.is_staff = True
        empleado.save()

        cliente_user, _ = User.objects.get_or_create(
            username="cliente@studshiny.com",
            defaults={"email": "cliente@studshiny.com", "first_name": "Cliente Demo StudShiny"},
        )
        cliente_user.set_password("cliente123")
        cliente_user.is_staff = False
        cliente_user.save()

        cliente, _ = Cliente.objects.update_or_create(
            correo="cliente@studshiny.com",
            defaults={
                "usuario": cliente_user,
                "nombre_completo": "Cliente Demo StudShiny",
                "tipo_documento": "Cedula de ciudadania",
                "numero_documento": "1000000001",
                "edad": 22,
                "tipo_sangre": "O+",
                "telefono": "3001234567",
                "contacto_emergencia": "Mama 3007654321",
                "tipo_perforacion_interes": "Septum",
                "alergias_patologias": "Sin alergias registradas",
                "numero_perforaciones": 2,
            },
        )

        productos = [
            ("Aro circular titanio", "Circular", "Titanio", "Plateado", "16G", "8 mm", 45000, 20, "core/images/circular-steel.jpeg"),
            ("Labret acero quirurgico", "Labret", "Acero Quirurgico", "Plateado", "16G", "10 mm", 30000, 15, "core/images/labret-steel.jpeg"),
            ("Barbell recto acero", "Barbell", "Acero Quirurgico", "Plateado", "14G", "32 mm", 55000, 8, "core/images/barbell-steel.jpeg"),
            ("Septum dorado con zirconias", "Septum", "Oro", "Dorado", "16G", "8 mm", 70000, 5, "core/images/septum-gold.jpeg"),
            ("Curved barbell plateado", "Curved Barbell", "Titanio", "Plateado", "16G", "10 mm", 48000, 3, "core/images/curved-barbell.jpeg"),
        ]
        creados = {}
        for nombre, categoria, material, color, calibre, medida, precio, stock, imagen in productos:
            producto, _ = Producto.objects.update_or_create(
                nombre=nombre,
                defaults={
                    "categoria": categoria,
                    "material": material,
                    "color": color,
                    "calibre": calibre,
                    "medida": medida,
                    "precio": precio,
                    "stock": stock,
                    "stock_minimo": 5,
                    "imagen": imagen,
                    "descripcion": "Joya corporal seleccionada para perforaciones seguras, con acabado pulido y estilo StudShiny.",
                },
            )
            creados[nombre] = producto

        for nombre, descripcion, precio in [
            ("Basico", "Una perforacion con kit de limpieza y joya basica.", 50000),
            ("Estandar", "Dos perforaciones para una misma persona con kit de limpieza.", 90000),
            ("VIP", "Cinco perforaciones con joyas basicas o titanio y cuidados incluidos.", 150000),
        ]:
            Promocion.objects.update_or_create(nombre=nombre, defaults={"descripcion": descripcion, "precio": precio, "activa": True})

        procedimiento, _ = Procedimiento.objects.update_or_create(
            cliente=cliente,
            tipo_perforacion="Septum",
            defaults={
                "nombre_cliente": cliente.nombre_completo,
                "telefono_cliente": cliente.telefono,
                "fecha_cita": timezone.now() + timezone.timedelta(days=3),
                "estado": "CONFIRMADA",
                "estado_pago": True,
                "notas_cuidados": "Limpiar con solucion salina dos veces al dia y evitar manipular la joya.",
                "joya_utilizada": creados["Septum dorado con zirconias"],
            },
        )
        Factura.objects.update_or_create(cliente=cliente, procedimiento=procedimiento, defaults={"total": 70000, "metodo_pago": "PSE", "pagada": True})

        for titulo, imagen in [
            ("Piercing labial", "core/images/home-collage.jpeg"),
            ("Joyería circular", "core/images/circular-steel.jpeg"),
        ]:
            GaleriaTrabajo.objects.update_or_create(titulo=titulo, defaults={"imagen": imagen, "visible": True})

        ConfiguracionEstudio.objects.get_or_create(nombre="StudShiny")
        self.stdout.write(self.style.SUCCESS("Datos iniciales cargados."))
