from flask import Flask, jsonify
from dotenv import load_dotenv
import os
load_dotenv()


# Crear la aplicación Flask
app = Flask(__name__)

# Definir rutas (endpoints)
@app.route("/")
def home():
    """Ruta principal que retorna un mensaje de bienvenida"""
    return jsonify({
        "mensaje": "¡Bienvenido a mi primer servicio web con Flask!",
        "status": "success"
    })

@app.route("/saludo/<nombre>")
def saludo(nombre):
    """
    Ruta que retorna un saludo personalizado
    
    Args:
        nombre (str): Nombre de la persona a saludar
    """
    return jsonify({
        "mensaje": f"¡Hola, {nombre}! Bienvenido al servicio web con Flask.",
        "status": "success"
    })

@app.errorhandler(404)
def not_found(error):
    """Manejador para errores 404"""
    return jsonify({
        "mensaje": "Ruta no encontrada",
        "status": "error"
    }), 404

@app.errorhandler(500)
def server_error(error):
    """Manejador para errores 500"""
    return jsonify({
        "mensaje": "Error interno del servidor",
        "status": "error"
    }), 500

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
