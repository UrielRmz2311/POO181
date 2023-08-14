from flask import Flask, render_template, request, redirect, url_for,flash,session, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user,logout_user,login_required, UserMixin

app = Flask(__name__)
app.secret_key='mysecretapp'
try: 
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] ='root'
    app.config['MYSQL_PASSWORD']=''
    app.config['MYSQL_DB']='bdconsultorio'
    app.secret_key = 'mysecretkey'
    mysql = MySQL(app)
    print("Conexion exitosa")
except Exception as ex:
    print(ex)

#Ruta principal ------------------------------
@app.route('/')
def login():
    return render_template('login.html') 

# Creamos la clase pare guardar el Usuario para las interface
class User(UserMixin):
    def __init__(self, id, Vrfc ,Vpass):
        self.id = id
        self.Vrfc = Vrfc
        self.Vpass = Vpass
    
    def get_id(self):
        return str(self.id)
#Obliga a iniciar sesion 
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message= 'Acceso denegado... Inicia Sesión para acceder'

#Guardamos la sesion 
@login_manager.user_loader
def load_user(id):
    print('Este es mi id:' + id)
    CS = mysql.connection.cursor()
    CS.execute('Select id, rfc, contraseña from medicos where id =%s', (id,))
    usuario = CS.fetchone()
    if usuario:
        print("Método: load_user(id), el usuario si coincide.")
        return User(id=usuario[0], Vrfc=[1], Vpass=[6])
    return None


#Metodo inisiar sesion --------------------------------------------------
@app.route('/iniciosesion', methods=['POST'])
def iniciosesion():
    if request.method == 'POST':
        rfc = request.form['txtusuario']
        contraseña = request.form['txtpass']
        
        if rfc == "" or contraseña == "":
            flash('No se puede entrar con campos vacios')
            return render_template('login.html')
        else:
            CS = mysql.connection.cursor()
            # Consulta para verificar las credenciales del usuario
            consulta = "SELECT * FROM medicos WHERE rfc = %s"
            CS.execute(consulta,(rfc,))
            usuario = CS.fetchone()
            mysql.connection.commit()
            # Iniciar sesión exitosa
            if usuario:
                row = usuario[6]
                rol = usuario[7]
                if check_password_hash(row,contraseña):
                    session['rol'] = rol  # Almacena el rol en la sesión
                    user = User(id=usuario[0], Vrfc=[1], Vpass=[6])
                    print(user)
                    login_user(user)
                    flash('Ingresar medico')
                    return redirect(url_for('inicio'))
                else:
                    flash('Contraseña incorrecta, favor de reintentar...')
                    return render_template('login.html')
            else:
                flash('RFC ingresado no existe, favor de reintentar...')
                return render_template('login.html')
                
# Cerrar sesion incluyendo el usuario con la sesion guardada------
@app.route('/Cerrarsesion')
def cerrarsesion():
    logout_user()
    flash("Sesion cerrada correctamente...")
    return redirect(url_for('login'))

@app.route('/ConsultorioMedico')
@login_required
def inicio():
    return render_template('inicio.html')

# ---------------------------  Opciones administrador ---------------------------------------
@app.route('/RegistroMedico')
@login_required
def interfazM():
    if session:
        rol = session.get('rol')  # Obtenemos el rol de la sesión
        if rol == 1:
            return render_template('formmedico.html')
        else:
            flash('No es administrador')
            return render_template('inicio.html')
    else:
        return render_template('login.html')

@app.route('/RegistrarMedico', methods=['POST'])
@login_required
def registrarM():
    if request.method == 'POST':
        Vnombre= request.form['txtNombre']
        Vapellido= request.form['txtApellido']
        Vcedula= request.form['txtcedula']
        Vrfc= request.form['txtrfc']
        Vcorreo= request.form['txtcorreo']
        Vcontrasena= request.form['txtpass']
        Vpass= request.form['txtpassw']
        Vrol= request.form['txtrol']
        #print(Vnombre,Vapellido,Vcedula,Vrfc,Vcontrasena,Vpass,Vrol)

        if Vnombre == "" or Vapellido == "" or Vcedula == "" or Vrfc == "" or Vapellido == "" or Vcontrasena == "" or Vpass == "" or Vrol == "Elegir...":
            flash('No se pueden guardar campos vacios')
            return render_template('formmedico.html')
        else:
            if Vcontrasena == Vpass:
                Encrippass = generate_password_hash(Vcontrasena, 'pbkdf2:sha256')
                print(check_password_hash(Encrippass,Vcontrasena))
                #Conectar y ejecutar el insert
                CS = mysql.connection.cursor()
                CS.execute('insert into medicos(rfc,nombre,apellidos,cedula,correo,contraseña,rol) values (%s,%s,%s,%s,%s,%s,%s)',(Vrfc,Vnombre,Vapellido,Vcedula,Vcorreo,Encrippass,Vrol))
                mysql.connection.commit()
                flash('El médico se guardo correctamente')
                return render_template('formmedico.html')
            else:
                flash('Las contraseñas no coinciden, favor de reintentar')
                return render_template('formmedico.html')


@app.route('/ConsultarMedico')
@login_required
def consulta():
    rol = session.get('rol')  # Obtenemos el rol de la sesión
    if rol == 1:
        CC= mysql.connection.cursor()
        CC.execute('select * from medicos')
        medicos= CC.fetchall()
        return render_template('cmedico.html', listamedico = medicos)
    else:
        flash('No es administrador')
        return render_template('inicio.html')

#Consultamos por nombre-------------------------------------------------
@app.route('/Consultanombre', methods=['POST'])
@login_required
def consultanombre():
    Varbuscar= request.form['txtbuscar']
    CC= mysql.connection.cursor()
    CC.execute('select * from medicos where nombre LIKE %s', (f'%{Varbuscar}%',))
    medicos= CC.fetchall()
    return render_template('cmedico.html', listamedico = medicos)

# Ruta editar médico -------------------------------------------------
@app.route('/editar/<id>')
@login_required
def editarmedico(id):
    CSid = mysql.connection.cursor()
    CSid.execute('select * from medicos where id = %s', (id,))
    Consid = CSid.fetchone()
    return render_template('amedico.html', med= Consid) 

@app.route('/actualizar/<id>', methods=['POST'])
@login_required
def actualizar(id):
    if request.method == 'POST':
        Vnombre= request.form['txtNombre']
        Vapellido= request.form['txtApellido']
        Vcedula= request.form['txtcedula']
        Vrfc= request.form['txtrfc']
        Vcorreo= request.form['txtcorreo']
        Vcontrasena= request.form['txtpass']
        Vpass= request.form['txtpassw']
        Vrol= request.form['txtrol']
        
        if Vnombre == "" or Vapellido == "" or Vcedula == "" or Vrfc == "" or Vcontrasena == "" or Vpass == "" or Vrol == "Elegir...":
            flash('No se pueden actualizar campos vacios')
            #Regresamos a la interfaz y con ella los datos ya insertados
            CSid = mysql.connection.cursor()
            CSid.execute('select * from medicos where id = %s', (id,))
            Consid = CSid.fetchone()
            return render_template('amedico.html', med= Consid) 
        else:
            CSid = mysql.connection.cursor()
            CSid.execute('select * from medicos where id = %s', (id,))
            Consid = CSid.fetchone()
            passwo = Consid[6]
            #Comparamos la contraseña con la BD para ver si son iguales
            if passwo==Vcontrasena:
                CSedit= mysql.connection.cursor()
                CSedit.execute('update medicos set rfc= %s, nombre= %s, apellidos= %s, cedula= %s, correo= %s, contraseña= %s, rol= %s where id= %s', (Vrfc, Vnombre, Vapellido, Vcedula, Vcorreo, Vcontrasena, Vrol, id,))
                mysql.connection.commit()
                
                CC = mysql.connection.cursor()
                CC.execute('select * from medicos')
                medicos = CC.fetchall()
                flash('El Médico se actualizó correctamente')
                return render_template('cmedico.html', listamedico=medicos)
            else:
                #Si el usuario introduce nuevas contraseñas, se comparan 
                if Vcontrasena == Vpass:
                    Encrippass = generate_password_hash(Vcontrasena, 'pbkdf2:sha256')
                    print(check_password_hash(Encrippass,Vcontrasena))
            
                    CSedit= mysql.connection.cursor()
                    CSedit.execute('update medicos set rfc= %s, nombre= %s, apellidos= %s, cedula= %s, correo= %s, contraseña= %s, rol= %s where id= %s', (Vrfc, Vnombre, Vapellido, Vcedula, Vcorreo, Encrippass, Vrol, id,))
                    mysql.connection.commit()
                    
                    CC = mysql.connection.cursor()
                    CC.execute('select * from medicos')
                    medicos = CC.fetchall()
                    flash('El Médico se actualizó correctamente')
                    return render_template('cmedico.html', listamedico=medicos)
                else:
                    flash('Las contraseñas no coinciden')
                    CSid = mysql.connection.cursor()
                    CSid.execute('select * from medicos where id = %s', (id,))
                    Consid = CSid.fetchone()
                    return render_template('amedico.html', med= Consid)
        
# Eliminar médico -------------------------------------------------------
@app.route('/borrar/<id>', methods=['POST'])
@login_required
def eliminar(id):
    if request.method == 'POST':
        CSeli = mysql.connection.cursor()
        CSeli.execute('delete from medicos where id= %s',(id,))
        mysql.connection.commit()
        return jsonify({'message': 'success'})
    return jsonify({'message': 'error'})

#---------------------------------------------------------------------------------------------------------

#------------------------------------- Pacientes --------------------------------------------------------
@app.route('/Expedientepaciente')
@login_required
def introexpac():
    return render_template('expaciente.html')

#---------------- Registrar pacientes ------------------------------------------------------------------
@app.route('/Registropaciente', methods=['POST'])
@login_required
def Registropaciente():
    if request.method == 'POST':
        Vcedula = request.form['txtcedula']
        Vnombre = request.form['txtNombre']
        Vapellido = request.form['txtApellido']
        Vnacimiento = request.form['txtnacimiento']
        Venfermedades = request.form['txtenfermedades'] if 'txtenfermedades' in request.form else ""
        Valergias = request.form['txtalergias'] if 'txtalergias' in request.form else ""
        Vantecedentes = request.form['txtantecedentes'] if 'txtantecedentes' in request.form else ""
        #print(Vcedula, Vnombre, Vapellido, Vnacimiento, Venfermedades, Valergias, Vantecedentes)
        
        if Vcedula == "" or Vnombre == "" or Vapellido =="" or Vnacimiento == "" or Venfermedades == "" or Valergias == "" or Vantecedentes == "":
            flash('No se pueden guardar campos vacíos')
            return render_template('expaciente.html')  
        else:      
            CSid = mysql.connection.cursor()
            CSid.execute('SELECT cedula FROM medicos WHERE cedula=%s', (Vcedula,))
            Consid = CSid.fetchone()
            if Consid is None:
                flash('La cédula ingresada no existe en la base de datos')
                return render_template('expaciente.html')
            else:
                if Venfermedades == 'Otra':
                    Venfermedadesotro = request.form['txtenfermedades_otro']
                    if Venfermedadesotro == "":
                        flash('No se pueden guardar campos vacíos')
                        return render_template('expaciente.html')
                    else:
                        Venfermedades = Venfermedadesotro

                if Valergias == 'Otro':
                    Valergiasotro = request.form['txtalergias_otro']
                    if Valergiasotro == "":
                        flash('No se pueden guardar campos vacíos')
                        return render_template('expaciente.html')
                    else:
                        Valergias = Valergiasotro

                if Vantecedentes == 'Otro':
                    Vantecedentesotro = request.form['txtantecedentes_otro']
                    if Vantecedentesotro == "":
                        flash('No se pueden guardar campos vacíos')
                        return render_template('expaciente.html')
                    else:
                        Vantecedentes = Vantecedentesotro
                CS = mysql.connection.cursor()
                CS.execute('insert into pacientes(cedulamedico,nombre,apellidos,fechanacimiento,enfermedades,alergias,antecedentes) values (%s,%s,%s,%s,%s,%s,%s)', (Vcedula, Vnombre, Vapellido, Vnacimiento, Venfermedades, Valergias, Vantecedentes))
                mysql.connection.commit()
                flash('El paciente se guardó correctamente')
                return render_template('expaciente.html')
            
# Ruta Exploracion y diagnostigo ---------------------------------------------------
@app.route('/Exploracion')
def exploracion():
    return render_template('exploracion.html')

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