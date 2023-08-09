from flask import Flask, render_template, request, redirect, url_for,flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] ='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='bdconsultorio'
app.secret_key = 'mysecretkey'
mysql = MySQL(app)

@app.route('/')
def login():
    return render_template('login.html') 

@app.route('/iniciosesion', methods=['GET','POST'])
def iniciosesion():
    if request.method == 'POST':
        print(request.form['txtusuario'])
        print(request.form['txtpass'])
        return render_template('inicio.html')
    else:
        return render_template('login.html')

@app.route('/ConsultorioMedico')
def inicio():
    return render_template('inicio.html')

@app.route('/RegistroMedico')
def interfazM():
    return render_template('formmedico.html')

@app.route('/RegistrarMedico', methods=['POST'])
def registrarM():
    if request.method == 'POST':
        Vnombre= request.form['txtNombre']
        Vapellido= request.form['txtApellido']
        Vcedula= request.form['txtcedula']
        Vrfc= request.form['txtrfc']
        Vcontrasena= request.form['txtpass']
        Vpass= request.form['txtpassw']
        Vrol= request.form['txtrol']
        #print(Vnombre,Vapellido,Vcedula,Vrfc,Vcontrasena,Vpass,Vrol)

        if Vnombre == "" or Vapellido == "" or Vcedula == "" or Vrfc == "" or Vapellido == "" or Vcontrasena == "" or Vpass == "" or Vrol == "":
            flash('No se pueden guardar campos vacios')
            return render_template('formmedico.html')
        else:
            if Vcontrasena == Vpass:
                #Conectar y ejecutar el insert
                CS = mysql.connection.cursor()
                CS.execute('insert into medicos(rfc,nombre,apellidos,cedula,correo,contraseña,rol) values (%s,%s,%s,%s,%s,%s,%s)',(Vtitulo,Vartista,Vanio))
                mysql.connection.commit()
                flash('El médico se guardo correctamente')
                return render_template('formmedico.html')
            else:
                flash('Las contraseñas no coinciden, favor de reintentar')
                return render_template('formmedico.html')


@app.route('/EdificioB')
def edificioB():
    return render_template('edificiob.html')

@app.route('/EdificioC')
def edificioC():
    return render_template('edificioc.html')

@app.route('/Biblioteca')
def Biblio():
    return render_template('biblioteca.html')

@app.route('/CAPTA')
def capta():
    return render_template('capta.html')

@app.route('/CIDEA')
def cidea():
    return render_template('cidea.html')

@app.route('/LakafeUPQ')
def cafeteria():
    return render_template('cafeteria.html')

@app.route('/LT')
def lt1():
    return render_template('LT1.html')

@app.route('/Talleres')
def talleres():
    return render_template('talleres.html')

@app.route('/Canchas')
def canchas():
    return render_template('canchas.html')

@app.route('/admision')
def registroproceso():
    return render_template('ADMISION.html')


if __name__ == '__main__':
    app.run(port=5600,debug=True)