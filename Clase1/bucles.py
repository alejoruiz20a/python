numeros = [1,0,2,23,4,5,87,7,8,0,100,0,12]

print("RANGE")
for i in range(len(numeros)):
    print(numeros[i])

print("SINGULAR")
for numero in numeros:
    if numero%2==0:
        print(numero)

print("WHILE")
i = 0
while i < len(numeros):
    print(numeros[i])
    i = i + 1

# PRACTICAR LOS SIGUIENTES CODIGOS
# SUCESIÓN DE FIBONACCI (0,1,1,2,3,5,8,13,21)