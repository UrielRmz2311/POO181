# Importacion de framework -------------------------------------------
from flask import Flask,render_template,request,redirect,url_for,flash
# Importacion de MySQL con FLASK
from flask_mysqldb import MySQL

# Inicialización del APP ó servidor ----------------------------------
app= Flask(__name__)

# Conexion de la base de datos ---------------------------------------
app.config['MYSQL_HOST']='localhost'
#app.config['MYSQL_USER']='root' # Usuario de MySQL 
#app.config['MYSQL_PASSWORD']=''  # Contraseña MySQL
#app.config['MYSQL_DB']='dbflask'  # Nombre de la base de datos
#app.secret_key='mysecretkey'
#mysql= MySQL(app)

# Declaración de las rutas hhtp://localhost:5000 ---------------------

  # Ruta principal -------------
@app.route('/')
def index():
    return render_template('index.html')

# ruta http:localhost:500/guardar tipo POST para Insert
@app.route('/guardar')
def guardar():
    return "Se guardo en la BD"

@app.route('/eliminar')
def eliminar():
    return "Se elimino en la BD"

# Ejecución de Servidor en el Puerto 5000 ---------------------------- 
if __name__ == "__main__":
    app.run(port=5000,debug=True)
    
