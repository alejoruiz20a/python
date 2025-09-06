from tiempo_completo import EmpleadoTiempoCompleto
from por_horas import EmpleadoPorHoras

empleadoTC1 = EmpleadoTiempoCompleto("Alejandro", "Amador", 30000000)
empleadoPH1 = EmpleadoPorHoras("Isabela", "Zuluaga", 100000, 70)

print(empleadoTC1._generar_id())
print(empleadoPH1)