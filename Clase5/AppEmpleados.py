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
        tk.Label(frame_form, text=("Nombre: ")).grid(row=0, column=0, padx=5, pady=5)

# INICIAR APLICACION
if __name__ == "__main__":
    root = tk.Tk()
    app = AppEmpleados(root)
    root.mainloop()