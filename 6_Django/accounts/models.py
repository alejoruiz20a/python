from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Usuario(models.Model):
    username = models.CharField(max_length=30, unique=True, verbose_name='Username')
    email = models.EmailField(unique=True, verbose_name='Email')
    nombre = models.CharField(max_length=30, verbose_name='Nombre')
    apellido = models.CharField(max_length=50, verbose_name='Apellido')
    password = models.CharField(max_length=128, verbose_name='Contraseña')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    is_active = models.BooleanField(default=True, verbose_name='¿Activo?')

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def save(self, *args, **kwargs):
        if not self.password.startswith('bcrypt$'):
            self.set_password(self.password)
        super().save(*args, **kwargs)