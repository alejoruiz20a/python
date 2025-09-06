from empleado import Empleado

class EmpleadoTiempoCompleto(Empleado): # HERENCIA
    def __init__(self, nombre, apellido, salario_anual):
        super().__init__(nombre, apellido) 
        self._salario_anual = salario_anual

    def calcular_salario(self):
        return self._salario_anual / 12
    
    #Getters y Setters

    @property
    def salario_anual(self):
        return self.salario_anual
    
    @salario_anual.setter
    def salario_anual(self, salario_anual):
        self._salario_anual = salario_anual

    # DEFINIR LA IMPRESIÓN

    def __str__(self):
        return f"Empleado Tiempo Completo {self._nombre} {self._apellido} gana {self.calcular_salario()} al mes."