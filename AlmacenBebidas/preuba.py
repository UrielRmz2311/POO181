import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Creamos un Combobox con valores predefinidos
values = ("opción 1", "opción 2", "opción 3")
combo = ttk.Combobox(root, values=values)
combo.pack()

# Creamos una función que se ejecutará cuando se seleccione una opción del Combobox
def get_selected_value():
    selected_value = combo.get()
    print("La opción seleccionada es:", selected_value)

# Creamos un botón que llamará a la función get_selected_value cuando sea presionado
button = tk.Button(root, text="Obtener valor seleccionado", command=get_selected_value)
button.pack()

root.mainloop()