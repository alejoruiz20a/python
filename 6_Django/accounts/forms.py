from django import forms
from .models import Usuario
import html

class RegistroForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Nombre de Usuario'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label = 'Correo Electrónico'
    )
    nombre = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Nombre',
        required=False
    )
    apellido = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Apellido',
        required=False
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Contraseña',
        min_length=8
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirmar Contraseña',
        min_length=8
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username = html.escape(username.strip())

        if len(username) < 3:
            raise forms.ValidationError('El usuario debe tener al menos 3 caracteres')
        
        if Usuario.objects.filter(username = username).exists():
            raise forms.ValidationError('Este usuario ya existe.')
        
        return username
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = html.escape(email.strip().lower())

        if Usuario.objects.filter(email = email).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        
        return email

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '')
        return html.escape(nombre.strip())
    
    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido', '')
        return html.escape(apellido.strip())
    
    def clean_password(self): 
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        
        return cleaned_data
    
class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label = 'Correo Electrónico'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Contraseña',
    )

    mantener_sesion = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Mantener sesión iniciada'
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = html.escape(email.strip().lower()) # Prevención contra todo tipo de injection
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if not password:
            raise forms.ValidationError('La contraseña es requerida')
        return password