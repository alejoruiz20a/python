import tkinter as tk
from tkinter import ttk, messagebox
from db import *

class AppEmpleados:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Empleados")
        self.root.geometry("800x600")

        # VARIABLES DE CONTROL
        self.id_empleado = tk.StringVar()
        self.nombre = tk.StringVar()
        self.cedula = tk.StringVar()
        self.cargo = tk.StringVar()
        self.sueldo = tk.DoubleVar() 

        # FRAME DEL FORMULARIO
        frame_form = tk.LabelFrame(root, text = "Datos del Empleado")
        frame_form.pack(padx=10, pady=10, fill="x")

        # CAMPOS DEL FORMULARIO
        #NOMBRE
        tk.Label(frame_form, text=("Nombre: ")).grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.nombre, width=40).grid(row=0, column=1, padx=5, pady=5)
        #CEDULA
        tk.Label(frame_form, text=("Cédula: ")).grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.cedula, width=40).grid(row=1, column=1, padx=5, pady=5)
        #CARGO
        tk.Label(frame_form, text=("Cargo: ")).grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.cargo, width=40).grid(row=2, column=1, padx=5, pady=5)
        #SUELDO
        tk.Label(frame_form, text=("Sueldo: ")).grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.sueldo, width=40).grid(row=3, column=1, padx=5, pady=5)

        # BOTONES DEL CRUD
        frame_botones = tk.Frame(root)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Guardar", command=self.guardar_empleado).grid(row=0, column=0, padx=5) # GUARDAR
        tk.Button(frame_botones, text="Editar", command=self.editar_empleado).grid(row=0, column=1, padx=5) # EDITAR
        tk.Button(frame_botones, text="Eliminar", command=self.eliminar_empleado).grid(row=0, column=2, padx=5) # ELIMINAR
        tk.Button(frame_botones, text="Limpiar", command=self.limpiar_campos).grid(row=0, column=3, padx=5) # LIMPIAR
        
        # TABLA DE EMPLEADOS
        frame_tabla = tk.LabelFrame(root, text="Lista de Empleados")
        frame_tabla.pack(pady=10, padx=10) #ahorita

        self.tabla = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Cédula", "Cargo", "Sueldo"), show="headings")
        self.tabla.pack(pady=10, padx=10)

        # Configurar las columnas
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Cédula", text="Cédula")
        self.tabla.heading("Cargo", text="Cargo")
        self.tabla.heading("Sueldo", text="Sueldo")

        self.tabla.column("ID", width=50)
        self.tabla.column("Nombre", width=220)
        self.tabla.column("Cédula", width=170)
        self.tabla.column("Cargo", width=170)
        self.tabla.column("Sueldo", width=150)

        # SCROLLBAR
        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        scroll.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scroll.set)

        # SELECCIÓN
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_empleado)

        # CARGAR DATOS DE LA TABLA
        self.actualizar_tabla()

    def guardar_empleado(self):
        if not self.validar_campos():
            return
        
        if self.id_empleado.get(): # SI HAY UN ID, SE ACTUALIZA
            actualizar_empleado(
                self.id_empleado.get(),
                self.nombre.get(),
                self.cedula.get(),
                self.cargo.get(),
                self.sueldo.get()
            )
            messagebox.showinfo("ÉXITO", "Empleado actualizado correctamente.")
        else:  # SI NO HAY UN ID, SE CREA UN EMPLEADO NUEVO
            try:
                crear_empleado(
                    self.nombre.get(),
                    self.cedula.get(),
                    self.cargo.get(),
                    self.sueldo.get()
                )
                messagebox.showinfo("ÉXITO", "Empleado creado con éxito.")
            except sqlite3.IntegrityError:
                messagebox.showerror("ERROR", "Ya existe un empleado con esa cédula.")
        
        self.limpiar_campos()
        self.actualizar_tabla()

    def editar_empleado(self):
        if not self.id_empleado.get():
            messagebox.showerror("ERROR", "Seleccione un empleado para editar.")
            return
        self.guardar_empleado()

    def eliminar_empleado(self):
        if not self.id_empleado.get():
            messagebox.showerror("ERROR", "Seleccione un empleado para eliminarlo.")
            return
        
        if messagebox.askyesno("ADVERTENCIA", f"¿Estás seguro de que deseas eliminar al empleado {self.nombre.get()}?"):
            eliminar_empleado(self.id_empleado.get())
            messagebox.showinfo("ÉXITO", "Empleado eliminado correctamente.")
            self.limpiar_campos()
            self.actualizar_tabla()

    def limpiar_campos(self):
        self.id_empleado.set("")
        self.nombre.set("")
        self.cedula.set("")
        self.cargo.set("")
        self.sueldo.set(0.0)

    def validar_campos(self):
        if not self.nombre.get() or not self.cedula.get() or not self.cargo.get():
            messagebox.showerror("ERROR", "Todos los campos son obligatorios.")
            return False
        try:
            float(self.sueldo.get())
        except:
            messagebox.showerror("ERROR", "El sueldo debe ser un número válido.")
            return False
        return True

    def seleccionar_empleado(self, event):
        item = self.tabla.selection()

        if item:
            datos = self.tabla.item(item, "values") # datos = [campo0, campo1, campo2, campo3, campo4]
            self.id_empleado.set(datos[0])
            self.nombre.set(datos[1])
            self.cedula.set(datos[2])
            self.cargo.set(datos[3])
            self.sueldo.set(datos[4])

    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        empleados = leer_empleados()
        for empleado in empleados:
            self.tabla.insert("", "end", values=empleado)

# INICIAR APLICACION
if __name__ == "__main__":
    root = tk.Tk()
    app = AppEmpleados(root)
    root.mainloop()