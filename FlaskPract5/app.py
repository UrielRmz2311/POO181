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
    return render_template('index.htm', albums=conAlbums)

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

@app.route('/eliminar')
def eliminar():
    return "Se elimino en la BD"

# Ejecución de Servidor en el Puerto 5000 ---------------------------- 
if __name__ == '__main__':
    app.run(port=5000,debug=True)
    
