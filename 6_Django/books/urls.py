from django.urls import path
from . import views

urlpatterns = [
    path('like/<int:libro_id>/', views.toggle_like, name='toggle_like'),
    path('libro/<int:libro_id>/', views.detalle_libro, name='detalle_libro'),
    path('crear/', views.crear_libro, name='crear_libro')
]
