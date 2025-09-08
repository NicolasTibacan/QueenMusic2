# repository/repository.py
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from model.model import Song

class SongRepository:
    def __init__(self, session: Session):
        self.session = session

    # Lecturas
    def get_all(self) -> List[Song]:
        return list(self.session.execute(select(Song)).scalars())

    def get_by_id(self, song_id: int) -> Optional[Song]:
        return self.session.get(Song, song_id)

    def find_by_name(self, name: str) -> List[Song]:
        stmt = select(Song).where(Song.name.ilike(f"%{name}%"))
        return list(self.session.execute(stmt).scalars())

    def find_by_album(self, album: str) -> List[Song]:
        stmt = select(Song).where(Song.album.ilike(f"%{album}%"))
        return list(self.session.execute(stmt).scalars())

    def search(self, q: str) -> List[Song]:
        stmt = select(Song).where(
            (Song.name.ilike(f"%{q}%")) | (Song.album.ilike(f"%{q}%"))
        )
        return list(self.session.execute(stmt).scalars())

    # Escrituras
    def create(self, name: str, album: str, year: int) -> Song:
        song = Song(name=name, album=album, year=year)
        self.session.add(song)
        self.session.flush()  # obtiene id
        self.session.refresh(song)
        return song

    def update(self, song_id: int, *, name: Optional[str] = None,
               album: Optional[str] = None, year: Optional[int] = None) -> Optional[Song]:
        song = self.get_by_id(song_id)
        if not song:
            return None
        if name is not None:
            song.name = name
        if album is not None:
            song.album = album
        if year is not None:
            song.year = year
        self.session.flush()
        self.session.refresh(song)
        return song

    def delete(self, song_id: int) -> bool:
        song = self.get_by_id(song_id)
        if not song:
            return False
        self.session.delete(song)
        return True
