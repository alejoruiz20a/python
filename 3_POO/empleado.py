from abc import ABC, abstractmethod

class Empleado():
    def __init__(self, nombre, apellido):
        self._nombre = nombre
        self._apellido = apellido
        self._id = self._generar_id()

    @property
    def nombre_completo(self):
        return f"{self._nombre} {self._apellido}"
    
    def _generar_id(self):
        return hash(f"{self._nombre}{self._apellido}")
    
    @abstractmethod
    def calcular_salario(self):
        pass

    # ENCAPSULAMIENTO (CONVENCIÓN)
    # GETTERS Y SETTERS
    
    @property
    def nombre(self): # GETNOMBRE
        return self._nombre
    
    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def apellido(self):  # GETAPELLIDO
        return self._apellido

    @apellido.setter
    def apellido(self, apellido):
        self._apellido = apellido

