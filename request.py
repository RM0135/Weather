from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():
# Obtener los datos en formato JSON de la solicitud
    datos = request.get_json()
    nombre = datos.get("nombre")
    edad = datos.get("edad")

# Crear una respuesta
    respuesta = {
    "mensaje": f"Usuario {nombre} de {edad} años creado exitosamente."
    }
    return jsonify(respuesta)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
    # Mostrar la respuesta del servidor
        print("Datos enviados exitosamente. Respuesta del servidor:")
        print(response.json())
    else:
        print("Hubo un problema con la solicitud.")
        if response.status_code == 404:
            print("No se encontró el recurso solicitado.")
        elif response.status_code == 500:
            print("El servidor experimentó un error.")
        else:
            print("Algo salió mal.")