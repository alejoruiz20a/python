from django.contrib import admin
from .models import Libro

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'fecha_creacion', 'publicado']
    list_filter = ['publicado', 'fecha_creacion']
    search_fields = ['titulo', 'contenido', 'autor__username']
