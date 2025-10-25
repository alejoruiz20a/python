from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class Usuario(models.Model):
    username = models.CharField(max_length=30, unique=True, verbose_name='Username')
    email = models.EmailField(unique=True, verbose_name='Email')
    nombre = models.CharField(max_length=30, verbose_name='Nombre')
    apellido = models.CharField(max_length=50, verbose_name='Apellido')
    password = models.CharField(max_length=128, verbose_name='Contraseña')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    is_active = models.BooleanField(default=True, verbose_name='¿Activo?')

    intentos_fallidos = models.IntegerField(default=0)
    bloqueado_hasta = models.DateTimeField(null=True, blank=True)
    ultimo_intento = models.DateTimeField(null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def incrementar_intento_fallido(self):
        self.intentos_fallidos += 1
        self.ultimo_intento = timezone.now()

        if self.intentos_fallidos >= 5:
            self.bloqueado_hasta = timezone.now() + timezone.timedelta(minutes=1)

        self.save()
    
    def resetear_intentos(self):
        self.intentos_fallidos = 0
        self.bloqueado_hasta = None
        self.save()

    def esta_bloqueado(self):
        if self.bloqueado_hasta:
            if timezone.now() < self.bloqueado_hasta:
                return True
            else:
                self.resetear_intentos()
        return False

    def save(self, *args, **kwargs):
        if not self.password.startswith('bcrypt$'):
            self.set_password(self.password)
        super().save(*args, **kwargs)