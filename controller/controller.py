# controller/controller.py
# controller/controller.py
from flask import Flask, jsonify, request
from functools import wraps
import jwt
from Config.databse import SessionLocal, init_db
from repository.repository import SongRepository
from services.services import SongService, ValidationError, NotFoundError
from services.auth_service import SECRET_KEY, ALGORITHM
from controller.auth_controller import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)
init_db()

# --- Middleware JWT ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return jsonify({"error": "Token faltante"}), 401
        try:
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401
        return f(*args, **kwargs)
    return decorated

# --- Endpoints ---
@app.route("/songs", methods=["GET"])
def list_songs():
    # Público (solo visualización)
    svc, session = SongService(SongRepository(SessionLocal())), SessionLocal()
    try:
        songs = svc.list()
        session.commit()
        return jsonify([s.to_dict() for s in songs]), 200
    finally:
        session.close()

@app.route("/songs/search", methods=["GET"])
@token_required
def search_songs():
    svc, session = SongService(SongRepository(SessionLocal())), SessionLocal()
    try:
        q = request.args.get("q")
        name = request.args.get("name")
        album = request.args.get("album")
        songs = svc.list(q=q, name=name, album=album)
        session.commit()
        return jsonify([s.to_dict() for s in songs]), 200
    finally:
        session.close()

@app.route("/songs", methods=["POST"])
@token_required
def create_song():
    svc, session = SongService(SongRepository(SessionLocal())), SessionLocal()
    try:
        data = request.get_json()
        song = svc.create(data["name"], data["album"], int(data["year"]))
        session.commit()
        return jsonify(song.to_dict()), 201
    except ValidationError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()
