from flask import Flask, render_template, request, redirect, url_for,flash
from flask_mysqldb import MySQL

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

# @app.route('/iniciosesion', method=['POST'])
#def iniciosesion():
 #   if request.method == 'POST':
  #      Vrfc = request.form['txtxusuario']
   #     Vcorreo = request.form['txtpass']
if __name__ == '__main__':
    app.run(port=5600,debug=True)