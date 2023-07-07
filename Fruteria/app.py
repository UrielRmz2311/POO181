# Importacion de framework -------------------------------------------
from flask import Flask,render_template,request,redirect,url_for,flash
# Importacion de MySQL con FLASK
from flask_mysqldb import MySQL

# Inicialización del APP ó servidor ----------------------------------
app= Flask(__name__)

# Conexion de la base de datos ---------------------------------------
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root' # Usuario de MySQL 
app.config['MYSQL_PASSWORD']=''  # Contraseña MySQL
app.config['MYSQL_DB']='db_fruteria'  # Nombre de la base de datos
app.secret_key='mysecretkey'
mysql= MySQL(app)

# Declaración de las rutas hhtp://localhost:5000 ---------------------

  # Ruta principal -------------
@app.route('/')
def fruteria():
    return render_template('fruteria.html')

# ruta http:localhost:500/guardar tipo POST para Insert
@app.route('/guardar', methods=['POST'] )
def guardar():
    if request.method == 'POST':
    #Pasamos a variables el contenido de los input
        Varfruta= request.form['txtfruta']
        Vartempo= request.form['txttemporada']
        Varprecio= request.form['txtprecio']
        Varstock= request.form['txtstock']
        print(Varfruta,Vartempo,Varprecio,Varstock)
        
        #Conectar y ejecutar el insert
        CS = mysql.connection.cursor()
        CS.execute('insert into tbfrutas(fruta,temporada,precio,stock) values (%s,%s,%s,%s)',(Varfruta,Vartempo,Varprecio,Varstock))
        mysql.connection.commit()
    flash('La Fruta se registro correctamente')
    return redirect(url_for('fruteria'))

@app.route('/editar/<id>')
def editar(id):
    cursorId = mysql.connection.cursor()
    cursorId.execute('select * from tbfrutas where id= %s',(id,))
    consulId = cursorId.fetchone()
    return render_template('editarfruta.html', fruta = consulId)

@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        #Pasamos a variables el contenido de los input
        Varfruta= request.form['txtfruta']
        Vartempo= request.form['txttemporada']
        Varprecio= request.form['txtprecio']
        Varstock= request.form['txtstock']
    
        curAct = mysql.connection.cursor()
        curAct.execute('update tbfrutas set fruta= %s, temporada= %s, precio= %s, stock= %s where id= %s', (Varfruta,Vartempo,Varprecio,Varstock,id))
        mysql.connection.commit()
        
    flash('El album se actualizo correctamente')
    return redirect(url_for('consulta'))

@app.route('/eliminar/<id>')
def borrar(id):
    cursorId = mysql.connection.cursor()
    cursorId.execute('select * from tbfrutas where id= %s',(id,))
    consulId = cursorId.fetchone()
    return render_template('eliminarfruta.html', fruta = consulId)

@app.route('/borrar/<id>', methods=['POST'])
def eliminar(id):
    if request.method == 'POST':

        cursorAct = mysql.connection.cursor()
        cursorAct.execute('delete from tbfrutas where id= %s',(id,))
        mysql.connection.commit()
        
    flash('Se elimino la fruta correctamente')
    return redirect(url_for('consulta'))

@app.route('/Consulta')
def consulta():
    CC= mysql.connection.cursor()
    CC.execute('select * from tbfrutas')
    confruta= CC.fetchall()
    print(confruta)
    return render_template('consulta.html', listafruta = confruta)

@app.route('/Consult')
def Consult():
    return render_template('consultan.html')

@app.route('/Consultanombre', methods=['POST'])
def consultanombre():
    Varbuscar= request.form['txtbuscar']
    print(Varbuscar)
    CC= mysql.connection.cursor()
    CC.execute('select * from tbfrutas where fruta LIKE %s', (f'%{Varbuscar}%',))
    confruta= CC.fetchall()
    print(confruta)
    return render_template('consultan.html', listafruta = confruta)


# Ejecución de Servidor en el Puerto 5100 ---------------------------- 
if __name__ == '__main__':
    app.run(port=5100,debug=True)
    
