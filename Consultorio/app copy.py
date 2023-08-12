from flask import Flask, render_template, request, redirect, url_for,flash,session
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


@app.route('/')
def login():
    return render_template('login.html') 

class User(UserMixin):
    def __init__(self, id, Vrfc ,Vpass):
        self.id = id
        self.Vrfc = Vrfc
        self.Vpass = Vpass
    
    def get_id(self):
        return str(self.id)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message= 'Acceso denegado... Inicia Sesión para acceder'


@login_manager.user_loader
def load_user(id):
    print('Este es mi id:' + id)
    CS = mysql.connection.cursor()
    CS.execute('Select id, rfc, contraseña from medicos where id =%s', (id,))
    usuario = CS.fetchone()
    if usuario:
        print("Método: load_user(id), el usario si coincide.")
        return User(id=usuario[0], Vrfc=[1], Vpass=[6])
    return None



@app.route('/iniciosesion', methods=['POST'])
def iniciosesion():
    if request.method == 'POST':
        rfc = request.form['txtusuario']
        contraseña = request.form['txtpass']
        
        if rfc == "" or contraseña == "":
            flash('No se pueden enviar campos vacios')
            return render_template('login.html')
        else:
            CS = mysql.connection.cursor()
            # Consulta para verificar las credenciales del usuario
            consulta = "SELECT * FROM medicos WHERE rfc = %s"
            CS.execute(consulta,(rfc,))
            usuario = CS.fetchone()
            mysql.connection.commit()
            # Iniciar sesión exitosa
            # Aquí puedes establecer una sesión o tomar otras medidas según tus necesidades
            if usuario:
                row = usuario[6]
                rol = usuario[7]
                if check_password_hash(row,contraseña):
                    session['rol'] = rol  # Almacena el rol en la sesión
                    user = User(id=usuario[0], Vrfc=[1], Vpass=[6])
                    login_user(user)
                    return redirect(url_for('inicio'))
                else:
                    flash('Credenciales incorrectas, favor de reintentar...')
                    return render_template('login.html')
            else:
                flash('RFC ingresado no existe...')
                return render_template('login.html')

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
def interfazM():
    if session:
        rol = session.get('rol')  # Obtiene el rol de la sesión
        if rol == 1:
            return render_template('formmedico.html')
        else:
            return render_template('inicio.html')
    else:
        return render_template('login.html')

@app.route('/RegistrarMedico', methods=['POST'])
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
def consulta():
    rol = session.get('rol')  # Obtiene el rol de la sesión
    if rol == 1:
        CC= mysql.connection.cursor()
        CC.execute('select * from medicos')
        medicos= CC.fetchall()
        return render_template('cmedico.html', listamedico = medicos)
    else:
        return render_template('inicio.html')


@app.route('/Consultanombre', methods=['POST'])
def consultanombre():
    Varbuscar= request.form['txtbuscar']
    CC= mysql.connection.cursor()
    CC.execute('select * from medicos where nombre LIKE %s', (f'%{Varbuscar}%',))
    medicos= CC.fetchall()
    return render_template('cmedico.html', listamedico = medicos)

#---------------------------------------------------------------------------------------------------------

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