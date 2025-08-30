import sqlite3

def conectar_db():
    conexion = sqlite3.connect("Clase5/empleados.db")
    cursor = conexion.cursor()

    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS empleados (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nombre TEXT NOT NULL,
                   cedula TEXT UNIQUE NOT NULL,
                   cargo TEXT NOT NULL,
                   sueldo REAL NOT NULL)
                   ''')
    
    conexion.commit()
    return conexion
    
def crear_empleado(nombre, cedula, cargo, sueldo):  # CREATE
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("INSERT INTO empleados (nombre, cedula, cargo, sueldo) VALUES (?, ?, ?, ?)", (nombre, cedula, cargo, sueldo))

    conexion.commit()
    conexion.close()

def leer_empleados():       # READ
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM empleados")

    empleados = cursor.fetchall()
    conexion.close()
    return empleados

def actualizar_empleado(id_empleado, nombre, cedula, cargo, sueldo): # UPDATE
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("UPDATE empleados SET nombre=?, cedula=?, cargo=?, sueldo=? WHERE id=?", (nombre,cedula,cargo,sueldo,id_empleado))

    conexion.commit()
    conexion.close()

def eliminar_empleado(id_empleado): # DELETE
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM empleados WHERE id=?",(id_empleado))

    conexion.commit()
    conexion.close()