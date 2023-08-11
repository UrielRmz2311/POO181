from werkzeug.security import generate_password_hash, check_password_hash

Vcontrasena = 'JessicaBreton'
Encrippass = generate_password_hash(Vcontrasena, 'pbkdf2:sha256')
print(Encrippass)
print(check_password_hash(Encrippass,Vcontrasena))