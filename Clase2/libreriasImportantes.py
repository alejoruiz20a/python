import os
import math
# from os import getcwd
import random
from datetime import datetime

print("El directorio actual es: ", os.getcwd()) # Current Working Directory

# os.remove("C:/Repos/python/Clase2/test.json")

ruleta = [5,3,2,4,6,1]
bala = random.choice(ruleta)

# bala = random.randint(1,6)
# print("Bala elegida: ",bala)

opcion = 1
while opcion != 0: 
    opcion = int(input("Ingrese un numero del 1 al 6: "))
    if opcion == bala:
        print("Estas muerto") # Borrar system32
    else: 
        print("Te salvaste")

print("Fecha y Hora actuales: ", datetime.now())

print("El numero pi es: ", math.pi)

# ruleta = [1,2,3,4,5,6]

print(max(ruleta))
print(min(ruleta))
print(sum(ruleta))
print(sorted(ruleta))
print(ruleta)