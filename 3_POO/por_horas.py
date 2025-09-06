from empleado import Empleado

class EmpleadoPorHoras(Empleado):
    def __init__(self, nombre, apellido, horas_trabajadas, valor_hora):
        super().__init__(nombre, apellido)
        self._horas_trabajadas = horas_trabajadas
        self._valor_hora = valor_hora

    def calcular_salario(self):
        return self._horas_trabajadas * self._valor_hora

    # Getters y Setters

    @property
    def horas_trabajadas(self):
        return self._horas_trabajadas
    
    @horas_trabajadas.setter
    def horas_trabajadas(self, horas_trabajadas):
        self._horas_trabajadas = horas_trabajadas

    @property
    def valor_hora(self):
        return self._valor_hora

    @valor_hora.setter
    def valor_hora(self, valor_hora):
        self._valor_hora = valor_hora

    def __str__(self):
        return f"Empleado Por Horas {self._nombre} {self._apellido} gana {self.calcular_salario()} al mes."