# controller/auth_controller.py
from flask import Blueprint, request, jsonify
from Config.databse import SessionLocal
from repository.user_repository import UserRepository
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    session = SessionLocal()
    repo = UserRepository(session)
    service = AuthService(repo)
    try:
        data = request.get_json()
        user = service.register_user(data["username"], data["password"])
        session.commit()
        return jsonify(user.to_dict()), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@auth_bp.route("/login", methods=["POST"])
def login():
    session = SessionLocal()
    repo = UserRepository(session)
    service = AuthService(repo)
    try:
        data = request.get_json()
        token = service.login_user(data["username"], data["password"])
        return jsonify({"token": token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401
    finally:
        session.close()
