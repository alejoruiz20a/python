from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from .forms import RegistroForm, LoginForm
from .models import Usuario

def bienvenida(request):
    return HttpResponse("""
    <h1>¡Bienvenido a Wattpad!</h1>
    <p>Esta es tu primer vista en Django</p>
    <style>
        body {
            margin: 40px,
            background: #f0f8ff;
        }
    </style>
                        """)

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
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            mantener_sesion = form.cleaned_data['mantener_sesion']

            try:
                usuario = Usuario.objects.get(email=email)

                if usuario.check_password(password):
                    request.session['usuario_id'] = usuario.id
                    request.session['usuario_email'] = usuario.email
                    request.session['usuario_username'] = usuario.username
                    
                    if mantener_sesion: 
                        request.session.set_expiry(1209600) # 2 Semanas
                    else:
                        request.session.set_expiry(0) # 2 Semanas
                else:
                    form.add_error('password', 'Contraseña incorrecta')
            except Usuario.DoesNotExist:
                form.add_error('email', 'No existe usuario con este correo')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form' : form})