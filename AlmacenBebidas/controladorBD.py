from tkinter import messagebox
import sqlite3
import bcrypt

class controlBD:
    
    def __init__(self):
        pass
    
# Preparamos la conexion para usarla cuando sea necesario --------------------------------------
    def conexionBD(self):
        try:
            conexion=sqlite3.connect("D:/canel/Documents/GitHub/POO181/AlmacenBebidas/BDBebidas.db")
            print("Conectado BD")
            return conexion
        
        except sqlite3.OperationalError:
            print("No se pudo conectar")

# Metodo para Insertar ---------------------------------------------------------------------
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
    
# Metodo para eliminar bebida --------------------------------------------------------------
    def eliminarbebida(self, dato):
        conx = self.conexionBD()
        
        if(id == ""):
            messagebox.showwarning("Cuidado", "Favor de llenar el campo con nombre")
            conx.close()
        else:
            try:
                cursor = conx.cursor()
                sqlDelete = "DELETE FROM Bebidas WHERE nombre=?"
                
                cursor.execute(sqlDelete, (dato,))
                eliminarbebida = cursor.fetchall()
                conx.commit()
                conx.close()
                messagebox.showinfo("Exito!!", "El registro fue eliminado")
                
                return eliminarbebida
            
            except sqlite3.OperationalError:
                print("Error Consulta")
# ------------------------------------------------------------------------------------------------------
    def consultaBebida(self, bebida):
        # Llamar a la conexión
        conx = self.conexionBD()

        # Verificar que la bebida no esté vacía
        if bebida == "":
            messagebox.showwarning("Advertencia", "Revisa tu formulario, no puedes dejar campos vacíos")
            conx.close()
        else:
            try:
                # Preparar lo necesario para el select
                cursor = conx.cursor()
                sqlSelect = "SELECT * FROM Bebidas WHERE nombre = ?"

                # Ejecutar y guardar la consulta
                cursor.execute(sqlSelect, (bebida,))
                RSbebida = cursor.fetchall()
                conx.close()

                return RSbebida

            except sqlite3.OperationalError:
                print("Error de consulta")
    def consultaBebidaid(self,id):
        #1. Preparar la conexión
        conx= self.conexionBD()
        
        #2. Verificar el ID no este vació
        if(id == ""):
            messagebox.showwarning("Error ","Rellena el registro ID")
        else:
        #3. Proceder a buscar
            try:
                #4. Prepara lo necesario para el select
                cursor= conx.cursor()
                sqlSelect= "select * from Bebidas where id="+id
                
                #5. Ejecución y guardado de la consulta
                cursor.execute(sqlSelect)
                RSusuario= cursor.fetchall()
                conx.close()
                
                return RSusuario
                
            except sqlite3.OperationalError:
                print("Error Consulta") 

    def consultamarca(self, bebida):
        # Llamar a la conexión
        conx = self.conexionBD()

        # Verificar que la bebida no esté vacía
        if bebida == "":
            messagebox.showwarning("Advertencia", "Revisa tu formulario, no puedes dejar campos vacíos")
            conx.close()
        else:
            try:
                # Preparar lo necesario para el select
                cursor = conx.cursor()
                sqlSelect = "SELECT * FROM Bebidas WHERE marca = ?"

                # Ejecutar y guardar la consulta
                cursor.execute(sqlSelect, (bebida,))
                RSbebida = cursor.fetchall()
                conx.close()

                return RSbebida

            except sqlite3.OperationalError:
                print("Error de consulta")
# -----------------------------------------------------------------------------  
    def consultarBebidas(self):
        conx = self.conexionBD()
        cursor = conx.cursor()
        try:
            # Seleccionar todos los registros de la Base de Datos
            sqlConsulta = "select * from Bebidas"
            cursor.execute(sqlConsulta)
            Consulta = cursor.fetchall()
            conx.close()
            return Consulta
        except sqlite3.OperationalError:
            print("Error, No se encontro ninguna Bebida")

#Metodo para modificar cualquier registro --------------------------------------
    def modificarRegistro(self, id, nombre, clasificacion, marca, precio):
        conx = self.conexionBD()
        
        if(id == "" or nombre == "" or clasificacion == "" or marca == "" or precio == ""):
            messagebox.showwarning("Cuidado", "ningun campo puede estar vacio")
            conx.close()
        else:
            try:
                cursor = conx.cursor()
                nom = nombre
                clasi = clasificacion
                mar = marca
                pre = precio
                sqlActualizar = "UPDATE Bebidas SET nombre=?, clasificacion=?, marca=? , precio=? WHERE id=?"
                
                cursor.execute(sqlActualizar, [nom, clasi, mar,pre, id])
                nuevousuario = cursor.fetchall()
                conx.commit()
                conx.close()
                messagebox.showinfo("Exito!!", "La Bebida fue modificada")
                return nuevousuario
            
            except sqlite3.OperationalError:
                print("Error Consulta")
            