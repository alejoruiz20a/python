"""
URL configuration for wattpad project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import registro, registro_exitoso, login, pagina_principal, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registro/', registro, name='registro'),
    path('login/', login, name='login'),
    path('registro/exitoso', registro_exitoso, name='registro_exitoso'),
    path('principal/', pagina_principal, name='pagina_principal'),
    path('logout', logout, name='logout'),
    path('', login, name='home'),
    path('like/', include('books.urls')) # AQUÍ ESTABA EL ERROR
]
