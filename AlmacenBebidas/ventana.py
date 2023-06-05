from tkinter import *
from tkinter import ttk
import tkinter as tk
from controladorBD import *

# Crear una instancia de tipo controlador
controlador= controlBD()

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

   # 1. Segunda Ventana -----------------------------------------------------------------------
def cambiar_ventana():
    def cambiarainicio ():
        otras_op.withdraw()
        inicio.deiconify() 
    inicio.withdraw()
    otras_op = tk.Toplevel()
    # Ventana 2 ---------------------------------------------------------------
    otras_op.title("Almacén Bebidas (Operaciones)")
    otras_op.geometry("750x520")
    panel2=ttk.Notebook(otras_op)
    panel2.pack(fill="both",expand="yes")
    
    CalcularPrecio=ttk.Frame(panel2)
    CantidadMarca=ttk.Frame(panel2)
    CantidadClasi=ttk.Frame(panel2)
    volver=ttk.Frame(panel2)
    
    # 4 Buscar marca -------------------------------------------------------------------------
    def Buscarmarca():
        rsBebida = controlador.consultamarca(Marca.get())
        num_filas = len(rsBebida) # Contar el número de tuplas devueltas por la consulta
        tablam.delete(*tablam.get_children())
        for user in rsBebida:
            tablam.insert("", tk.END, text="", values=user)
        txtcant.insert("0.0",num_filas) # Mostrar el número de elementos en la tabla
            
    # Calcular precio ---------------------------------------------------------
    titulo5 = Label(CalcularPrecio, text = "Calcular Precio promedio de bebidas", fg = "green", font = ("Arial", 18)).pack()
    
    # Cantidad por Marca ------------------------------------------------------
    titulo6= Label(CantidadMarca, text = "Cantidad de bebidas de una Marca", fg = "blue", font = ("Arial", 18)).pack()
    
    Marca= tk.StringVar()
    marcan= Label(CantidadMarca, text="Marca de Bebida: ")
    marcan.pack()
    txtmarcas= Entry(CantidadMarca, textvariable=Marca)
    txtmarcas.pack()
    
    btnBuscarmarca = Button(CantidadMarca, text = "Buscar",command=Buscarmarca)
    btnBuscarmarca.pack()
    
    columns = ("id", "nombre", "clasificacion", "marca", "precio")
    tablam = ttk.Treeview(CantidadMarca, columns = columns, show = "headings")

    tablam.column("id", anchor=tk.W, width=30)
    tablam.column("nombre", anchor=tk.W, width=130)
    tablam.column("clasificacion", anchor=tk.W, width=130)
    tablam.column("marca", anchor=tk.W, width=130)
    tablam.column("precio", anchor=tk.W, width=180)

    tablam.heading("id", text = "ID", )
    tablam.heading("nombre", text = "NOMBRE")
    tablam.heading("clasificacion", text = "CLASIFICACIÓN")
    tablam.heading("marca", text = "MARCA")
    tablam.heading("precio", text = "PRECIO")

    tablam.pack()
    
    cantidamarca= Label(CantidadMarca, text = "Cantidad", fg = "blue", font = ("Arial", 12))
    cantidamarca.pack()
    txtcant = tk.Text(CantidadMarca, height = 2, width = 52)
    txtcant.pack()
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
    
   # 2. Guardar Bebida -----------------------------------------------------------------------
def ejecutaInsert():
    controlador.guardarBebida(varBe.get(),varClas.get(),varmar.get(), varPre.get())
    
# 4 Buscar Bebida -------------------------------------------------------------------------
def BuscarBebida():
    rsBebida = controlador.consultaBebida(Nomb.get())
        
    for usu in rsBebida:
        cadena = str(usu[0])+" "+ usu[1]+" "+ usu[2]+" "+usu[3]+" "+str(usu[4]) 
        
    if (rsBebida):
        txtbeb.insert("0.0",cadena)
    else:
        messagebox.showinfo("No encontrado", "Bebida no registrada en la BD")

# 5. Eliminar Bebida ----------------------------------------------------------------------
def ejecutaEliminar():
    sel = messagebox.askyesno("Eliminar Bebida", "Seguro que desea eliminar la Bebida?")
    if (sel == True):
        
        try:
            controlador.eliminarbebida(Nomb.get())
        except sqlite3.OperationalError:
            print("Error Consulta")
            
# 6. Consulta Bebidas --------------------------------------------------------------------
def ConsultarRegistros():
    Registrados = controlador.consultarBebidas()
    tabla.delete(*tabla.get_children())
    for user in Registrados:
        tabla.insert("", tk.END, text = "", values = user)

# 7 Actualizar Bebidas -------------------------------------------------------------------
def ejecutaModificar():
    rsUsuario = controlador.consultaBebidaid(varid.get())
    if(rsUsuario):
        controlador.modificarRegistro(varid.get(), varNombre.get(), varClasi.get(), varMarca.get(), varPrecio.get())
    else:
        messagebox.showinfo("No encontrado", "Usuario no registardo en la BD")
# Alta de Bebidas -------------------------------------------------------------
titulo= Label(alta,text="Alta de Bebidas", fg="Blue", font=("Arial",18)).pack()

varBe= tk.StringVar()
iblBe= Label(alta, text="Nombre Bebida y capacida (1L ,2L ,3L, etc.): ").pack()
txtBe= Entry(alta, textvariable=varBe).pack()


iblmClas= Label(alta, text= "Clasificación: ").pack()
values = ("Energetica", "Azucarada", "Agua","Alcoholica","Soda")
varClas= ttk.Combobox(alta, values=values)
varClas.pack()

varmar= tk.StringVar()
iblmar= Label(alta, text="Marca: ").pack()
txtmar= Entry(alta, textvariable=varmar).pack()

varPre= tk.DoubleVar()
iblPre= Label(alta, text="Precio: ").pack()
txtPre= Entry(alta, textvariable=varPre).pack()

btnGuardar= Button(alta, text="Registrar Bebida", command=ejecutaInsert).pack()

# Baja de Bebidas -------------------------------------------------------------
titulo = Label(baja, text = "Baja de Bebidas", fg = "red", font = ("Arial", 18)).pack()

Nomb= tk.StringVar()
iblnomb= Label(baja, text="Nombre Bebida: ").pack()
txtnomb= Entry(baja, textvariable=Nomb).pack()

btnBuscar = Button(baja, text = "Buscar",command=BuscarBebida)
btnBuscar.pack()

bebidaRe = Label(baja, text = "Bebida Registrada:", fg = "blue", font = ("Arial", 18)).pack()
txtbeb = tk.Text(baja, height = 2, width = 52)
txtbeb.pack()

btnBusqueda = tk.Button(baja, text = "Eliminar", command=ejecutaEliminar)
btnBusqueda.pack()

# Consulta de Bebidas ---------------------------------------------------------
titulo3 = Label(consulta, text = "Consulta de bebidas", fg = "red", font = ("Arial", 18)).pack()

columns = ("id", "nombre", "clasificacion", "marca", "precio")
tabla = ttk.Treeview(consulta, columns = columns, show = "headings")

tabla.column("id", anchor=tk.W, width=30)
tabla.column("nombre", anchor=tk.W, width=130)
tabla.column("clasificacion", anchor=tk.W, width=130)
tabla.column("marca", anchor=tk.W, width=130)
tabla.column("precio", anchor=tk.W, width=180)

tabla.heading("id", text = "ID", )
tabla.heading("nombre", text = "NOMBRE")
tabla.heading("clasificacion", text = "CLASIFICACIÓN")
tabla.heading("marca", text = "MARCA")
tabla.heading("precio", text = "PRECIO")

tabla.pack()

btnConsulta = Button(consulta, text = "Registros", command=ConsultarRegistros).pack()

# Actualizar Bebidas ----------------------------------------------------------
titulo4 = Label(actualizar, text = "Actualizar Bebidas", fg = "green", font = ("Arial", 18)).pack()

varid= tk.StringVar()
lblid = Label(actualizar, text = "ID de la bebida: ").pack()
txtid = Entry(actualizar, textvariable = varid).pack()

varNombre= tk.StringVar()
lblNombre = Label(actualizar, text = "Nombre Bebida (nuevo): ").pack()
txtNombre = Entry(actualizar, textvariable = varNombre).pack()

iblmClasi= Label(actualizar, text= "Clasificación (nueva): ").pack()
values2 = ("Energetica", "Azucarada", "Agua","Alcoholica","Soda")
varClasi= ttk.Combobox(actualizar, values=values2)
varClasi.pack()

varMarca= tk.StringVar()
lblMarca = Label(actualizar, text = "Marca (nueva): ").pack()
txtMarca = Entry(actualizar, textvariable = varMarca).pack()

varPrecio= tk.DoubleVar()
lblPrecio = Label(actualizar, text = "Precio (nuevo): ").pack()
txtPrecio = Entry(actualizar,textvariable = varPrecio).pack()

btnmodificar= Button(actualizar, text = "Actualizar", command=ejecutaModificar).pack()


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