from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'nombre', 'apellido', 'is_active', 'fecha_registro', 'intentos_fallidos', 'bloqueado_hasta', 'ultimo_intento']
    list_filter = ['is_active', 'fecha_registro']
    search_fields = ['username', 'email', 'nombre', 'apellido']