class Persona:
    def __init__(self, nombre, apellido, cedula, edad):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.edad = edad

    def nombreCompleto(self):
        return self.nombre+" "+self.apellido

persona1 = Persona("Alejo", "Amador", 10039173, 21)
persona2 = Persona("Carlos", "Martinez", 128907103, 75)

print("El nombre de la persona 1 es: ", persona1.nombreCompleto())
print("El nombre de la persona 2 es: ", persona2.nombre)