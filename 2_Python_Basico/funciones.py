# BASICO 
def Sumar2(a,b):
    return a + b

print(Sumar2(1,2))

# CON *ARGS
def Sumar(*args):
    suma = 0
    for arg in args:
        suma = suma + arg
    return suma

print(Sumar(1,2,3,4,5,6,7,8,9,10,11))

# CON AMBOS
def funcionDePrueba(a,b,*args):
    mul = a*b
    for arg in args:
        mul = mul + arg
    return mul

print(funcionDePrueba(3,5,2,6,8))

# CON VALORES PREDETERMINADOS
def potencia(a=1, b=2):
    return a**b

print(potencia(3,9))