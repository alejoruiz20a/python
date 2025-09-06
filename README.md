# Curso de Python
## Para iniciar un entorno virtual:
- python -m venv venv
- venv/Scripts/activate

## Para exportar con pyinstaller a exe
(revisar que la base de datos se cree bien)
- pip install pyinstaller
- cd ruta/del/proyecto
- pyinstaller --onefile --noconsole AppEmpleados.py 
y listo, ya tienes tu .exe en dist
si quieres exportarlo con icono, usa --icon="icon.ico" como atributo extra
* Pagina recomendada para iconos: icon-icons.com

