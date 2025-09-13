from django.db import models
from accounts.models import Usuario

class Libro(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    contenido = models.TextField(verbose_name='Contenido')
    autor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación') 
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Ultima Actualización') 
    publicado = models.BooleanField(default=True, verbose_name='¿Publicado?')

    def __str__(self):
        return f"{self.titulo} - por {self.autor.username}"