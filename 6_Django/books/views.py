from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .models import Libro, Like
from accounts.models import Usuario
from .forms import LibroForm

@csrf_protect
def toggle_like(request, libro_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    libro = get_object_or_404(Libro, id=libro_id, publicado = True)
    usuario = get_object_or_404(Usuario, id = request.session['usuario_id'])

    if libro.usuario_ya_dio_like(usuario):
        libro.quitar_like(usuario)
    else:
        libro.dar_like(usuario)

    return redirect('pagina_principal')

def detalle_libro(request, libro_id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    libro = get_object_or_404(Libro, id = libro_id, publicado = True)
    usuario = get_object_or_404(Usuario, id = request.session['usuario_id'])

    ya_tiene_like = libro.usuario_ya_dio_like(usuario)

    context = {
        'libro' : libro,
        'ya_tiene_like' : ya_tiene_like,
        'total_likes' : libro.total_likes,
        'usuario_username' : request.session['usuario_username']
    }

    return render(request, 'detalle_libro.html', context)

def crear_libro(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            libro = form.save(commit = False)

            usuario = get_object_or_404(Usuario, id = request.session['usuario_id'])
            libro.autor = usuario

            libro.save()

            messages.success(request, '¡Tu libro ha sido publicado exitosamente')
            return redirect('pagina_principal')
    else:
        form = LibroForm()

    context = {
        'form' : form,
        'usuario_username' : request.session['usuario_username']
    }

    return render(request, 'crear_libro.html', context)

def mis_libros(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    usuario_actual = get_object_or_404(Usuario, id = request.session['usuario_id'])
    libros = Libro.objects.filter(autor=usuario_actual).order_by('-fecha_creacion')

    context = {
        'libros' : libros,
        'usuario_username' : request.session['usuario_username'],
        'total_mis_libros' : libros.count()
    }

    return render(request, 'mis_libros.html', context)