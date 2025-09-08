# QueenMusic2
📂 Documentación de la Arquitectura
📁 Config/

Propósito: Manejo de configuración y conexión a la base de datos.

__init__.py
Archivo vacío para declarar el paquete Python.

database.py

Se encarga de crear la conexión a la base de datos.

Intenta conectarse primero a Supabase/Postgres usando la variable de entorno SUPABASE_DB_URL.

Si falla, hace fallback a una base local SQLite (queenmusic.db).

Define:

Base: clase base de SQLAlchemy para modelos.

engine: motor de conexión.

SessionLocal: creador de sesiones.

init_db(): inicializa las tablas.

get_session(): context manager para manejar sesiones.

📁 model/

Propósito: Representación de las entidades/tablas de la base de datos.

__init__.py
Archivo vacío.

model.py

Contiene la clase Song, que representa la tabla songs.

Campos:

id (Primary Key)

name (Nombre de la canción)

album (Nombre del álbum)

year (Año de publicación)

Incluye restricción de unicidad (name+album).

Tiene un método to_dict() para serializar la entidad en JSON.

📁 repository/

Propósito: Capa de acceso a datos.
Implementa consultas y operaciones CRUD sobre los modelos usando SQLAlchemy (ORM).

__init__.py
Archivo vacío.

repository.py

Clase SongRepository:

Lecturas:

get_all() → trae todas las canciones.

get_by_id() → busca por ID.

find_by_name() → busca por nombre parcial.

find_by_album() → busca por álbum parcial.

search() → búsqueda genérica por nombre o álbum.

Escrituras:

create() → crea un registro nuevo.

update() → actualiza datos de una canción existente.

delete() → elimina una canción.

📁 services/

Propósito: Lógica de negocio.
Usa el repositorio para aplicar reglas y validaciones antes de tocar la base de datos.

__init__.py
Archivo vacío.

services.py

Excepciones:

ValidationError → errores de reglas de negocio.

NotFoundError → cuando un registro no existe.

Clase SongService:

Valida que los campos sean correctos.

Evita duplicados (name+album).

Métodos:

list() → listar con filtros.

get() → obtener una canción.

create() → crear con validación.

update() → actualizar si existe.

delete() → eliminar si existe.

📁 controller/

Propósito: Capa de presentación (API HTTP).
Define endpoints REST usando Flask.

__init__.py
Archivo vacío.

controller.py

Define el objeto Flask app.

Rutas:

GET /songs → lista canciones (filtros: q, name, album).

GET /songs/<id> → obtiene canción por ID.

POST /songs → crea canción.

PUT/PATCH /songs/<id> → actualiza canción.

DELETE /songs/<id> → elimina canción.

Maneja excepciones (ValidationError, NotFoundError).

app.py (si decides mantenerlo aquí)

Punto de entrada para correr la API.

Inicializa la BD y arranca Flask en localhost:5000.

📂 Raíz del proyecto

README.md
Documentación general de la API, cómo instalar dependencias, variables de entorno, y cómo ejecutar.

requirements.txt
Lista de dependencias:

flask

sqlalchemy

psycopg2-binary (para Postgres/Supabase)

python-dotenv (opcional, si usas .env).

main.py (opcional)
Alternativa a app.py como punto de entrada principal del proyecto.