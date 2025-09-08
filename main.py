from controller.controller import app
from Config.databse import init_db

if __name__ == "__main__":
    # Inicializar la base de datos (crea tablas si no existen)
    init_db()

    # Ejecutar la aplicación Flask
    app.run(host="0.0.0.0", port=5000, debug=True)
