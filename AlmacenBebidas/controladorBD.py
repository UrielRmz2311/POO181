from tkinter import messagebox
import sqlite3
import bcrypt

class controlBD:
    
    def __init__(self):
        pass
    
    # Preparamos la conexion para usarla cuando sea necesario
    def conexionBD(self):
        try:
            conexion=sqlite3.connect("D:/canel/Documents/GitHub/POO181/AlmacenBebidas/BDBebidas.db")
            print("Conectado BD")
            return conexion
        
        except sqlite3.OperationalError:
            print("No se pudo conectar")

    # Metodo para Insertar
    def guardarBebida(self,nom,cla,mar,pre):
        # 1. Llamar a la conexion
        conx=self.conexionBD()
        
        # 2. Revisar que los parametros no esten vacios     
        if(nom == "" or cla == "" or mar == "" or pre == ""):
            messagebox.showwarning("Aguas!!!","Revisa tu formulario")
            conx.close()
        else:
            #3. Preparar los datos y el querySQL
            cursor= conx.cursor()
            datos=(nom,cla,mar,pre)
            qrInsert="insert into Bebidas(nombre,clasificacion,marca,precio) values(?,?,?,?)"
            
            #4. Proceder a Insertar y cerramos la conx conexion
            cursor.execute(qrInsert,datos)
            conx.commit()
            conx.close()
            messagebox.showinfo("Exito","Se guardo la Bebida")
    
            