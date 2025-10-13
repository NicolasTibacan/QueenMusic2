# repository/user_repository.py
from sqlalchemy.orm import Session
from model.user_model import User

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_username(self, username: str):
        return self.session.query(User).filter(User.username == username).first()

    def create_user(self, username: str, password_hash: str):
        user = User(username=username, password_hash=password_hash)
        self.session.add(user)
        self.session.flush()
        self.session.refresh(user)
        return user
