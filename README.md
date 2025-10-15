# 🎶 API REST — Música de Queen (con Autenticación JWT)
🧩 Descripción General

Esta API ofrece información musical sobre la legendaria banda Queen, permitiendo acceder a los álbumes, años de lanzamiento y canciones, protegida mediante un sistema de autenticación por tokens JWT (JSON Web Token).

Los usuarios deben autenticarse para consultar los recursos disponibles.
Los tokens tienen una validez de 3 horas.

Esta API utiliza una base de datos SQLite para almacenar la información musical y los usuarios registrados, ofreciendo un entorno ligero, rápido y fácil de desplegar.
Su estructura modular separa claramente la lógica de autenticación, las rutas de usuarios, las rutas de música y la configuración de la base de datos, lo que la convierte en una base sólida para proyectos educativos o de portafolio orientados al desarrollo de servicios REST seguros y bien estructurados.
📁 Descripción Detallada de Carpetas y Archivos
🔧 Config/

db.py
Este archivo configura la conexión a la base de datos SQLite y crea una sesión de SQLAlchemy.
Define la dependencia get_db() que permite acceder a la base de datos desde los controladores.

# 🎮 controller/

music_controller.py
Define las rutas (endpoints) de la API.
Aquí se controlan las solicitudes HTTP y se conectan con las funciones del repository o services.

Ejemplos de endpoints:

GET /songs → Lista todas las canciones.

GET /songs/{id} → Devuelve una canción por su ID.

POST /songs → Agrega una nueva canción (requiere token JWT).

POST /login → Autentica al usuario y genera un token.

Cada endpoint está documentado y validado mediante Pydantic Schemas para asegurar integridad en los datos.

# 🎵 model/

queen_models.py
Contiene las clases que representan las tablas de la base de datos:

User: almacena usuarios registrados y contraseñas encriptadas.

Song: contiene información de las canciones (título, álbum, año).

Usa SQLAlchemy para definir relaciones y tipos de datos, facilitando la manipulación ORM (sin escribir SQL manual).

# 🧠 repository/

music_repository.py
Es la capa encargada de interactuar directamente con la base de datos.
Implementa funciones CRUD:

Crear una nueva canción

Listar todas las canciones

Buscar por ID o nombre

Actualizar y eliminar registros

Esta capa aísla la lógica de persistencia, permitiendo mantener los controladores ligeros y más fáciles de probar.

# 🔐 services/

auth_service.py
Gestiona todo lo relacionado con autenticación y seguridad:

Validación de credenciales

Encriptación de contraseñas

Generación de tokens JWT con expiración de 3 horas

Decodificación y verificación de tokens para proteger rutas privadas

Usa la librería passlib para proteger contraseñas y jwt (o jose) para emitir tokens seguros.

🚀 main.py

Archivo principal que inicia el servidor FastAPI.

Importa y registra los controladores (rutas).

Conecta con la base de datos y prepara la documentación automática de la API
# 🧠 Conclusión

Esta API te permite:

Autenticar usuarios mediante JWT

Consultar y agregar canciones de Queen

Controlar acceso seguro a recursos

Integrar un backend ligero con base de datos local

Ideal para proyectos educativos, portafolios de desarrolladores o prácticas de autenticación con Python y FastAPI.