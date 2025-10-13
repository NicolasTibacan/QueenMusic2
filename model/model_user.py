# model/user_model.py
from sqlalchemy import Column, Integer, String
from Config.databse import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    def to_dict(self):
        return {"id": self.id, "username": self.username}
