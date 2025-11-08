from django import forms
import html
from .models import Libro

class LibroForm(forms.ModelForms):
    class Meta:
        model = Libro
        fields = ['titulo', 'contenido']

        widgets = {
            'titulo' : forms.TextInput(attrs= {
                'class' : 'form-control',
                'placeholder' : 'Título de tu historia'
            }),
            'contenido' : forms.Textarea(attrs={
                'class' : 'form-control',
                'placeholder' : 'Escribe tu historia aquí...',
                'rows' :  15
            })
        }

        labels = {
            'titulo' : 'Título',
            'contenido' : 'Contenido'
        }

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        titulo = html.escape(titulo.strip())

        if len(titulo) < 3:
            raise forms.ValidationError('El título debe tener al menos 3 caracteres')
        if len(titulo) > 200:
            raise forms.ValidationError('El titulo no debe exceder los 200 caracteres')
        
        return titulo
    
    def clean_contenido(self):
        contenido = self.cleaned_data.get('contenido')
        contenido = html.escape(contenido.strip())

        if len(contenido) < 1000:
            raise forms.ValidationError('El contenido debe tener al menos 1000 caracteres')
        
        return contenido
