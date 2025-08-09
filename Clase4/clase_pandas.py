import pandas as pd
import os

CANTIDAD_EMPLEADOS = 4

def leer_empleado(archivo):
    with open(archivo, 'r') as file: 
        lineas = file.readlines()

    datos = [linea.strip() for linea in lineas if linea.strip()] # LISTA COMPRENSIVA / LIST COMPREHENSION

    print(datos)

    if len(datos) == 5:
        return {
            'Nombre' : datos[0],
            'Cedula' : datos[1],
            'Anio' : datos[2],
            'Cargo': datos[3],
            'Salario' : datos[4]
        }
    else:
        print(f"Advertencia: El archivo {archivo} no contiene el formato esperado")
        return None
    
# DEFINIR ARCHIVOS
archivos = []
for i in range(CANTIDAD_EMPLEADOS):
    archivos.append(f"Clase4/Empleados/empleado{str(i+1)}.txt")

# VERIFICAR SI LOS ARCHIVOS EXISTEN    
archivos = [archivo for archivo in archivos if os.path.exists(archivo)]

datos_empleados = []
for archivo in archivos:
    empleado = leer_empleado(archivo)
    if empleado: 
        datos_empleados.append(empleado)

print(datos_empleados)

dataframe = pd.DataFrame(datos_empleados)
nombre_archivo_excel = "empleados.xlsx"
dataframe.to_excel(nombre_archivo_excel, index=False, sheet_name="Empleados")
print(f"Datos de empleados guardados exitosamente en {nombre_archivo_excel}")