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
app.config['MYSQL_DB']='dbflask'  # Nombre de la base de datos
app.secret_key='mysecretkey'
mysql= MySQL(app)

# Declaración de las rutas hhtp://localhost:5000 ---------------------

  # Ruta principal -------------
@app.route('/')
def index():
    CC= mysql.connection.cursor()
    CC.execute('select * from albums')
    conAlbums= CC.fetchall()
    print(conAlbums)
    return render_template('index.html', listalbums=conAlbums)

# ruta http:localhost:500/guardar tipo POST para Insert
@app.route('/guardar', methods=['POST'] )
def guardar():
    if request.method == 'POST':
    #Pasamos a variables el contenido de los input
        Vtitulo= request.form['txtTitulo']
        Vartista= request.form['txtArtista']
        Vanio= request.form['txtAnio']
        print(Vtitulo,Vartista,Vanio)
        
        #Conectar y ejecutar el insert
        CS = mysql.connection.cursor()
        CS.execute('insert into albums(titulo,artista,anio) values (%s,%s,%s)',(Vtitulo,Vartista,Vanio))
        mysql.connection.commit()
    flash('El album fue agregado correctamente')
    return redirect(url_for('index'))

@app.route('/editar/<id>')
def editar(id):
    cursorId = mysql.connection.cursor()
    cursorId.execute('select * from albums where id= %s',(id,))
    consulId = cursorId.fetchone()
    return render_template('editarAlbum.html', album = consulId)

@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        #Pasamos a variables el contenido de los input
        Vartitulo= request.form['txtTitulo']
        Vartista= request.form['txtArtista']
        Varanio= request.form['txtAnio']
    
        curAct = mysql.connection.cursor()
        curAct.execute('update albums set titulo= %s, artista= %s, anio= %s where id= %s', (Vartitulo,Vartista,Varanio,id))
        mysql.connection.commit()
        
    flash('El album se actualizo correctamente')
    return redirect(url_for('index'))

@app.route('/eliminar/<id>')
def borrar(id):
    cursorId = mysql.connection.cursor()
    cursorId.execute('select * from albums where id= %s',(id,))
    consulId = cursorId.fetchone()
    return render_template('eliminarAlbum.html', album = consulId)

@app.route('/borrar/<id>', methods=['POST'])
def eliminar(id):
    if request.method == 'POST':

        cursorAct = mysql.connection.cursor()
        cursorAct.execute('delete from albums where id= %s',(id,))
        mysql.connection.commit()
        
    flash('Se elimino el album correctamente')
    return redirect(url_for('index'))

# Ejecución de Servidor en el Puerto 5000 ---------------------------- 
if __name__ == '__main__':
    app.run(port=5000,debug=True)
    
