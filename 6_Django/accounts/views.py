from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from .forms import RegistroForm, LoginForm
from .models import Usuario
from books.models import Libro
from django.db.models import Count

@csrf_protect
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = Usuario(
                username = form.cleaned_data['username'],
                email = form.cleaned_data['email'],
                nombre = form.cleaned_data['nombre'],
                apellido = form.cleaned_data['apellido'],
                password = form.cleaned_data['password']
            )
            usuario.save()
            return redirect('registro_exitoso')
    else: 
        form = RegistroForm()

    return render(request, 'registro.html', {'form' : form})

def registro_exitoso(request):
    return render(request, 'registro_exitoso.html')

def login(request):
    if 'usuario_id' in request.session:
        return redirect('pagina_principal')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            mantener_sesion = form.cleaned_data['mantener_sesion']

            try:
                usuario = Usuario.objects.get(email=email)

                if usuario.esta_bloqueado():
                    form.add_error(None, 'Cuenta bloqueada temporalmente. Intenta en un minuto.')
                    return render(request, 'login.html', {'form': form})

                if usuario.check_password(password):
                    usuario.resetear_intentos()

                    request.session['usuario_id'] = usuario.id
                    request.session['usuario_email'] = usuario.email
                    request.session['usuario_username'] = usuario.username
                    
                    if mantener_sesion: 
                        request.session.set_expiry(1209600) # 2 Semanas
                    else:
                        request.session.set_expiry(0) # Cuando se cierra la pestaña

                    return redirect('pagina_principal')
                else:
                    usuario.incrementar_intento_fallido()

                    form.add_error('password', 'Credenciales Incorrectas')
            except Usuario.DoesNotExist:
                form.add_error('email', 'Credenciales Incorrectas')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form' : form})

def pagina_principal(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    orden = request.GET.get('orden', 'recientes')

    libros = Libro.objects.filter(publicado = True)

    if orden == 'likes':
        libros = libros.annotate(num_likes = Count('likes')).order_by('-num_likes')
    else:
        libros = libros.order_by('-fecha_creacion')

    usuario_id = request.session['usuario_id']
    usuario_username = request.session['usuario_username']

    usuario_actual = Usuario.objects.get(id = usuario_id)

    info_libros = []

    for libro in libros:
        info_libros.append({
            'libro' : libro,
            'ya_tiene_like' : libro.usuario_ya_dio_like(usuario_actual),
            'total_likes' : libro.total_likes
        })

    context = {
        'usuario_username' : usuario_username,
        'info_libros' : info_libros,
        'orden_actual' : orden,
        'total_libros' : libros.count()
    }

    return render(request, 'pagina_principal.html', context)

def logout(request):
    request.session.flush()
    return redirect('login')