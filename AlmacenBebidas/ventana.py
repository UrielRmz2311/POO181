from tkinter import *
from tkinter import ttk
import tkinter as tk

# Ventana 1 ------------------------------------------------------------------

inicio=Tk()
inicio.title("Almacén Bebidas")
inicio.geometry("750x320")

panel=ttk.Notebook(inicio)
panel.pack(fill="both",expand="yes")

alta=ttk.Frame(panel)
baja=ttk.Frame(panel)
consulta=ttk.Frame(panel)
actualizar=ttk.Frame(panel)
otras=ttk.Frame(panel)

# Metodos ---------------------------------------------------------------------

   # 1. -----------------------------------------------------------------------
def cambiar_ventana():
    def cambiarainicio ():
        otras_op.withdraw()
        inicio.deiconify() 
    inicio.withdraw()
    otras_op = tk.Toplevel()
    # Ventana 2 ---------------------------------------------------------------
    otras_op.title("Almacén Bebidas (Operaciones)")
    otras_op.geometry("750x320")
    panel2=ttk.Notebook(otras_op)
    panel2.pack(fill="both",expand="yes")
    
    CalcularPrecio=ttk.Frame(panel2)
    CantidadMarca=ttk.Frame(panel2)
    CantidadClasi=ttk.Frame(panel2)
    volver=ttk.Frame(panel2)
    # Calcular precio ---------------------------------------------------------
    titulo5 = Label(CalcularPrecio, text = "Calcular Precio promedio de bebidas", fg = "green", font = ("Arial", 18)).pack()
    
    # Cantidad por Marca ------------------------------------------------------
    titulo6= Label(CantidadMarca, text = "Cantidad de bebidas de una Marca", fg = "blue", font = ("Arial", 18)).pack()
    
    # Cantidad por Clasificación ----------------------------------------------
    titulo7= Label(CantidadClasi, text = "Cantidad por clasificación", fg = "red", font = ("Arial", 18)).pack()
    
    # Volver ------------------------------------------------------------------
    titulo8= Label(volver, text = "Volver a Ventana Inicio", fg = "red", font = ("Arial", 18)).pack()
    
    button = ttk.Button(volver, text="Cambiar a Inicio", command=cambiarainicio)
    button.pack(pady=10)    
    
    panel2.add(CalcularPrecio,text="Calcular Precio")
    panel2.add(CantidadMarca,text="Cantidad Marca")
    panel2.add(CantidadClasi,text="Cantidad Clasificación")
    panel2.add(volver,text="Regresar")
    
# Alta de Bebidas -------------------------------------------------------------
titulo= Label(alta,text="Alta de Bebidas", fg="Blue", font=("Arial",18)).pack()

varBe= tk.StringVar()
iblBe= Label(alta, text="Nombre Bebida: ").pack()
txtBe= Entry(alta, textvariable=varBe).pack()

varClas= tk.StringVar()
iblmClas= Label(alta, text= "Clasificación: ").pack()
varClas = ("Energetica", "Azucarada", "Agua","Alcoholica","Soda")
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
titulo = Label(baja, text = "Baja de Bebidas", fg = "red", font = ("Arial", 18)).pack()
 
ID= tk.StringVar()
lblID= Label(baja, text = "Nombre de la bebida: ").pack()
txtID= Entry(baja, textvariable = ID).pack()

btnBuscar = Button(baja, text = "Buscar").pack()

usuarioRe = Label(baja, text = "Bebida Registrada:", fg = "blue", font = ("Arial", 18)).pack()
txtusu = tk.Text(baja, height = 2, width = 52)
txtusu.pack()

btnBusqueda = Button(baja, text = "Eliminar").pack()

# Consulta de Bebidas ---------------------------------------------------------
titulo3 = Label(consulta, text = "Consulta de bebidas", fg = "red", font = ("Arial", 18)).pack()

columns = ("id", "nombre", "correo", "marca", "contra")
tabla = ttk.Treeview(consulta, columns = columns, show = "headings")

tabla.column("id", anchor=tk.W, width=50)
tabla.column("nombre", anchor=tk.W, width=150)
tabla.column("correo", anchor=tk.W, width=150)
tabla.column("marca", anchor=tk.W, width=150)
tabla.column("contra", anchor=tk.W, width=200)

tabla.heading("id", text = "ID", )
tabla.heading("nombre", text = "NOMBRE")
tabla.heading("correo", text = "CLASIFICACIÓN")
tabla.heading("marca", text = "MARCA")
tabla.heading("contra", text = "PRECIO")

tabla.pack()

btnConsulta = Button(consulta, text = "Registros").pack()

# Actualizar Bebidas ----------------------------------------------------------
titulo4 = Label(actualizar, text = "Actualizar Bebidas", fg = "green", font = ("Arial", 18)).pack()

varid= tk.StringVar()
lblid = Label(actualizar, text = "ID de la bebida: ").pack()
txtid = Entry(actualizar, textvariable = varid).pack()

varNombre= tk.StringVar()
lblNombre = Label(actualizar, text = "Nombre Bebida (nuevo): ").pack()
txtNombre = Entry(actualizar, textvariable = varNombre).pack()

varClasi= tk.StringVar()
lblClasi= Label(actualizar, text = "Clasificación (nueva): ").pack()
txtClasi = Entry(actualizar, textvariable = varClasi).pack()

varMarca= tk.StringVar()
lblMarca = Label(actualizar, text = "Marca (nueva): ").pack()
txtMarca = Entry(actualizar, textvariable = varMarca).pack()

varPrecio= tk.StringVar()
lblPrecio = Label(actualizar, text = "Precio (nuevo): ").pack()
txtPrecio = Entry(actualizar, textvariable = varPrecio).pack()

btnmodificar= Button(actualizar, text = "Actualizar").pack()


# Otras Opciones --------------------------------------------------------------
titulo4 = Label(otras, text = "Otras Opciones", fg = "purple", font = ("Arial", 18)).pack()

text1= Label(otras, text = "Calcular Precio promedio de bebidas", fg = "green", font = ("Arial", 12)).pack()

text2= Label(otras, text = "Cantidad de bebidas de una Marca", fg = "blue", font = ("Arial", 12)).pack()

text3= Label(otras, text = "Cantidad por clasificación", fg = "red", font = ("Arial", 12)).pack()

button = ttk.Button(otras, text="Cambiar a operaciones", command=cambiar_ventana)
button.pack(pady=10)

panel.add(alta,text="Alta de Bebidas")
panel.add(baja,text="Baja de Bebidas")
panel.add(consulta,text="Consulta de Bebidas")
panel.add(actualizar,text="Actualizar Bebida")
panel.add(otras,text="Otras Opciones")
inicio.mainloop()