# services/services.py
from typing import List, Optional
from repository.repository import SongRepository
from model.model import Song

class ValidationError(Exception):
    pass

class NotFoundError(Exception):
    pass

class SongService:
    """
    Orquesta la lógica de negocio y usa el repositorio para acceso a datos.
    """
    def __init__(self, repo: SongRepository):
        self.repo = repo

    # Reglas de negocio / validaciones
    def _validate_fields(self, name: str, album: str, year: int):
        if not name or not album:
            raise ValidationError("Nombre y Álbum son obligatorios.")
        if not isinstance(year, int):
            raise ValidationError("El año debe ser numérico.")
        if year < 1900 or year > 2100:
            raise ValidationError("El año debe estar entre 1900 y 2100.")

    def list(self, id: Optional[int] = None, name: Optional[str] = None,
             album: Optional[str] = None) -> List[Song]:
        if id:
            return self.repo.search(id)
        if name:
            return self.repo.find_by_name(name)
        if album:
            return self.repo.find_by_album(album)
        return self.repo.get_all()

    def get(self, song_id: int) -> Song:
        song = self.repo.get_by_id(song_id)
        if not song:
            raise NotFoundError("Canción no encontrada.")
        return song

    def create(self, name: str, album: str, year: int) -> Song:
        self._validate_fields(name, album, year)
        # Evitar duplicados (name+album)
        existing = self.repo.search(name)
        for s in existing:
            if s.name.lower() == name.lower() and s.album.lower() == album.lower():
                raise ValidationError("La canción ya existe en ese álbum.")
        return self.repo.create(name=name, album=album, year=year)

    def update(self, song_id: int, *, name: Optional[str] = None,
               album: Optional[str] = None, year: Optional[int] = None) -> Song:
        if year is not None:
            self._validate_fields(name or "tmp", album or "tmp", year)  # valida solo año si faltan campos
        updated = self.repo.update(song_id, name=name, album=album, year=year)
        if not updated:
            raise NotFoundError("Canción no encontrada para actualizar.")
        return updated

    def delete(self, song_id: int) -> None:
        ok = self.repo.delete(song_id)
        if not ok:
            raise NotFoundError("Canción no encontrada para eliminar.")
