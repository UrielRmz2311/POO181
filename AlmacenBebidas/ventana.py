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




panel.add(alta,text="Alta de Bebidas")
panel.add(baja,text="Baja de Bebidas")
panel.add(consulta,text="Consulta de Bebidas")
panel.add(actualizar,text="Actualizar Bebida")
inicio.mainloop()