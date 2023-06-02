from tkinter import *
from tkinter import ttk
import tkinter as tk

inicio=Tk()
inicio.title("Almacén Bebidas")
inicio.geometry("500x300")

panel=ttk.Notebook(inicio)
panel.pack(fill="both",expand="yes")

alta=ttk.Frame(panel)
baja=ttk.Frame(panel)
consulta=ttk.Frame(panel)
actualizar=ttk.Frame(panel)

# Metodos ---------------------------------------------------------------------

# Alta de Bebidas -------------------------------------------------------------
titulo= Label(alta,text="Alta de Bebidas", fg="Blue", font=("Arial",18)).pack()

varBe= tk.StringVar()
iblBe= Label(alta, text="Nombre Bebida: ").pack()
txtBe= Entry(alta, textvariable=varBe).pack()

iblmClas= Label(alta, text= "Clasificación: ").pack()
varClas = ("Energetica", "Azucarada", "Agua","Alcoholica","Soda","Otra")
combo = ttk.Combobox(alta, values=varClas)
combo.pack()

varmar= tk.StringVar()
iblmar= Label(alta, text="Marca: ").pack()
txtmar= Entry(alta, textvariable=varmar).pack()

varPre= tk.StringVar()
iblPre= Label(alta, text="Precio: ").pack()
txtPre= Entry(alta, textvariable=varPre).pack()

btnGuardar= Button(alta, text="Registrar Bebida").pack()
# Baja de Bebidas -------------------------------------------------------------


# Consulta de Bebidas ---------------------------------------------------------


# Actualizar Bebidas ----------------------------------------------------------

panel.add(alta,text="Alta de Bebidas")
panel.add(baja,text="Baja de Bebidas")
panel.add(consulta,text="Consulta de Bebidas")
panel.add(actualizar,text="Actualizar Bebida")
inicio.mainloop()