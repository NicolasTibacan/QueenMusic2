# model/model.py
from sqlalchemy import Column, Integer, String, UniqueConstraint
from Config.databse import Base

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    album = Column(String(255), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("name", "album", name="uq_song_album"),
    )

    def to_dict(self):
        return {"id": self.id, "name": self.name, "album": self.album, "year": self.year}
