from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Config.base import Base
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from model.model import Song  



def _make_engine(db_url: str):
    # Para SQLite se necesita connect_args para hilos; para Postgres no.
    connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}
    return create_engine(db_url, echo=False, future=True, pool_pre_ping=True, connect_args=connect_args)

def get_engine():
    """
    Intenta conectarse a Supabase (variable de entorno SUPABASE_DB_URL).
    Si falla, hace fallback a SQLite local.
    """
    supabase_url = os.getenv("SUPABASE_DB_URL", "").strip()
    if supabase_url:
        try:
            engine = _make_engine(supabase_url)
            # Probar conexión
            with engine.connect() as conn:
                conn.exec_driver_sql("SELECT 1;")
            print("[DB] Conectado a Supabase/Postgres.")
            return engine
        except OperationalError as e:
            print(f"[DB] No fue posible conectar a Supabase. Fallback a SQLite. Detalle: {e}")

    sqlite_url = os.getenv("SQLITE_DB_URL", "sqlite:///queenmusic.db")
    engine = _make_engine(sqlite_url)
    print("[DB] Usando SQLite local.")
    return engine

engine = get_engine()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

def init_db():
    """
    Crea las tablas si no existen. Importa el modelo aquí para que
    el mapeo esté registrado en Base.metadata.
    """
   
    Base.metadata.create_all(bind=engine)
