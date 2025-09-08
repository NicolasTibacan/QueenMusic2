# controller/controller.py
from flask import Flask, jsonify, request
from sqlalchemy.exc import IntegrityError
from Config.databse import SessionLocal, init_db
from repository.repository import SongRepository
from services.services import SongService, ValidationError, NotFoundError

app = Flask(__name__)
init_db()

def service_with_session():
    """
    Crea una sesión por request y devuelve (service, session).
    El controlador se encarga de cerrar/confirmar.
    """
    session = SessionLocal()
    repo = SongRepository(session)
    svc = SongService(repo)
    return svc, session

@app.teardown_request
def remove_session(exception=None):
    """
    Asegura cierre de la sesión si se guardó en el objeto request.
    (Defensivo: el código ya cierra manualmente en cada endpoint.)
    """
    sess = getattr(request, "_db_session", None)
    if sess is not None:
        sess.close()

# ---- Rutas ----

@app.route("/songs", methods=["GET"])
def list_songs():
    svc, session = service_with_session()
    try:
        q = request.args.get("q")
        name = request.args.get("name")
        album = request.args.get("album")
        songs = svc.list(q=q, name=name, album=album)
        session.commit()
        return jsonify([s.to_dict() for s in songs]), 200
    finally:
        session.close()

@app.route("/songs/<int:song_id>", methods=["GET"])
def get_song(song_id: int):
    svc, session = service_with_session()
    try:
        song = svc.get(song_id)
        session.commit()
        return jsonify(song.to_dict()), 200
    except NotFoundError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 404
    finally:
        session.close()

@app.route("/songs", methods=["POST"])
def create_song():
    svc, session = service_with_session()
    try:
        payload = request.get_json(force=True) or {}
        name = payload.get("name")
        album = payload.get("album")
        year = payload.get("year")
        # Aceptar año como string y convertir
        if isinstance(year, str) and year.isdigit():
            year = int(year)
        song = svc.create(name=name, album=album, year=int(year))
        session.commit()
        return jsonify(song.to_dict()), 201
    except (ValidationError, ValueError) as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    except IntegrityError as e:
        session.rollback()
        return jsonify({"error": "Violación de unicidad (name+album)."}), 409
    finally:
        session.close()

@app.route("/songs/<int:song_id>", methods=["PUT", "PATCH"])
def update_song(song_id: int):
    svc, session = service_with_session()
    try:
        payload = request.get_json(force=True) or {}
        name = payload.get("name")
        album = payload.get("album")
        year = payload.get("year")
        if year is not None and isinstance(year, str) and year.isdigit():
            year = int(year)
        song = svc.update(song_id, name=name, album=album, year=year)
        session.commit()
        return jsonify(song.to_dict()), 200
    except (ValidationError, ValueError) as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    except NotFoundError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 404
    finally:
        session.close()

@app.route("/songs/<int:song_id>", methods=["DELETE"])
def delete_song(song_id: int):
    svc, session = service_with_session()
    try:
        svc.delete(song_id)
        session.commit()
        return jsonify({"message": "Eliminado"}), 200
    except NotFoundError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 404
    finally:
        session.close()

# Ejecución local:
# if __name__ == "__main__":
#     app.run(debug=True)
