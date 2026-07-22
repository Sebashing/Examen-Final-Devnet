import sqlite3
import hashlib
from flask import Flask

app = Flask(__name__)

# Función para transformar la contraseña en un Hash seguro
def generar_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Función para crear la base de datos y almacenar los usuarios
def configurar_base_datos():
    conexion = sqlite3.connect('usuarios.db')
    cursor = conexion.cursor()
    
    # Crear la tabla si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       usuario TEXT UNIQUE,
                       password_hash TEXT)''')
    
    # Limpiar tabla para evitar duplicados en cada ejecución
    cursor.execute("DELETE FROM usuarios")
    
    # Insertar los dos usuarios solicitados (Sebastián y uno a elección)
    usuarios_nuevos = [
        ("Sebastián Costas", generar_hash("cisco123")),
        ("AdminPrueba", generar_hash("admin123"))
    ]
    
    cursor.executemany("INSERT INTO usuarios (usuario, password_hash) VALUES (?, ?)", usuarios_nuevos)
    conexion.commit()
    conexion.close()

# Función para validar los usuarios
def validar_usuario(usuario, password):
    conexion = sqlite3.connect('usuarios.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT password_hash FROM usuarios WHERE usuario=?", (usuario,))
    resultado = cursor.fetchone()
    conexion.close()
    
    if resultado:
        hash_guardado = resultado[0]
        if hash_guardado == generar_hash(password):
            return True
    return False

# Ruta principal del servidor web
@app.route('/')
def inicio():
    return "<h1>Sitio Web Activo</h1><p>El servidor web esta funcionando correctamente en el puerto 5800.</p>"

if __name__ == '__main__':
    print("1. Configurando Base de Datos y hashes...")
    configurar_base_datos()
    
    print("\n2. Validación de Usuarios (Comando respectivo)")
    user = input("Ingrese el nombre de usuario a validar: ")
    pwd = input("Ingrese la contraseña: ")
    
    if validar_usuario(user, pwd):
        print("-> Validación Exitosa: El usuario y contraseña coinciden en la base de datos.")
    else:
        print("-> Error: Credenciales incorrectas.")
        
    print("\n3. Iniciando el servidor web en el puerto 5800...")
    # Se levanta el servidor web en el puerto 5800
    app.run(port=5800)