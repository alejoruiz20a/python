from django.shortcuts import render
from django.http import HttpResponse

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
