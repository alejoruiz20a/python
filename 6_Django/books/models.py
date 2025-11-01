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
    
    @property
    def total_likes(self):
        return self.likes.count()
    
    def usuario_ya_dio_like(self, usuario):
        return self.likes.filter(usuario=usuario).exists()
    
    def dar_like(self, usuario):
        if not self.usuario_ya_dio_like(usuario):
            Like.objects.create(libro = self, usuario = usuario)
            return True
        return False
    
    def quitar_like(self, usuario):
        like = self.likes.filter(usuario = usuario).first()

        if like:
            like.delete()
            return True
        return False

class Like(models.Model):
    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='likes_dados'
    )
    fecha_like = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.usuario.username} le dió like a {self.libro.titulo}'
    