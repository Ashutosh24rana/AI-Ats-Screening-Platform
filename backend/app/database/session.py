"""Compatibility shim — prefer importing from app.database.database."""

from app.database.database import Base, SessionLocal, engine, get_db  # noqa: F401

__all__ = ["Base", "SessionLocal", "engine", "get_db"]
