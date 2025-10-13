# services/auth_service.py
import datetime
import bcrypt
import jwt
from repository.user_repository import UserRepository

SECRET_KEY = "super_secret_key_queen"  # ⚠️ Usa variable de entorno en producción
ALGORITHM = "HS256"
TOKEN_EXP_HOURS = 3

class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))

    def generate_token(self, username: str) -> str:
        exp = datetime.datetime.utcnow() + datetime.timedelta(hours=TOKEN_EXP_HOURS)
        payload = {"sub": username, "exp": exp}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def decode_token(self, token: str) -> str:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]

    def register_user(self, username: str, password: str):
        if self.repo.get_by_username(username):
            raise ValueError("El usuario ya existe.")
        hash_ = self.hash_password(password)
        return self.repo.create_user(username, hash_)

    def login_user(self, username: str, password: str):
        user = self.repo.get_by_username(username)
        if not user or not self.verify_password(password, user.password_hash):
            raise ValueError("Credenciales incorrectas.")
        return self.generate_token(username)
