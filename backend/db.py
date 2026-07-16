from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backend.config import config


class Base(DeclarativeBase):
    pass


def _make_engine():
    config.ensure_dirs()
    engine = create_engine(
        f"sqlite:///{config.db_path}",
        connect_args={"check_same_thread": False, "timeout": 30},
    )

    @event.listens_for(engine, "connect")
    def _set_pragmas(dbapi_conn, _record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine


engine = _make_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def init_db() -> None:
    from backend import models  # noqa: F401  (register tables)

    Base.metadata.create_all(engine)
    _migrate()


def _migrate() -> None:
    """Additive schema migrations for databases created by older versions."""
    new_columns = {
        "activities": [
            ("is_workout", "BOOLEAN NOT NULL DEFAULT 0"),
            ("avg_power_w", "FLOAT"),
            ("avg_vertical_oscillation_mm", "FLOAT"),
            ("avg_vertical_ratio_pct", "FLOAT"),
            ("avg_step_length_mm", "FLOAT"),
            ("avg_stance_time_ms", "FLOAT"),
            ("avg_respiration_brpm", "FLOAT"),
            ("gap_speed_mps", "FLOAT"),
            ("decoupling_pct", "FLOAT"),
            ("efficiency_index", "FLOAT"),
            ("weather_temp_c", "FLOAT"),
            ("weather_humidity_pct", "FLOAT"),
            ("weather_wind_mps", "FLOAT"),
            ("weather_code", "INTEGER"),
            ("tag", "VARCHAR"),
            ("user_note", "VARCHAR NOT NULL DEFAULT ''"),
            ("name_locked", "BOOLEAN NOT NULL DEFAULT 0"),
        ],
        "laps": [("intensity", "VARCHAR")],
        "athlete_settings": [
            ("zone_mode", "VARCHAR NOT NULL DEFAULT 'max_hr'"),
            ("manual_zone_bounds", "JSON"),
            ("rtss_use_gap", "BOOLEAN NOT NULL DEFAULT 1"),
            ("pace_zone_mode", "VARCHAR NOT NULL DEFAULT 'threshold'"),
            ("manual_pace_zone_bounds", "JSON"),
            ("coaching_tone", "VARCHAR NOT NULL DEFAULT 'balanced'"),
            ("display_locale", "VARCHAR NOT NULL DEFAULT ''"),
        ],
        "streams": [
            ("power", "JSON"),
            ("vertical_oscillation", "JSON"),
            ("vertical_ratio", "JSON"),
            ("step_length", "JSON"),
            ("stance_time", "JSON"),
            ("respiration", "JSON"),
        ],
    }
    with engine.connect() as conn:
        for table, columns in new_columns.items():
            existing = {row[1] for row in conn.exec_driver_sql(f"PRAGMA table_info({table})")}
            for name, ddl in columns:
                if name not in existing:
                    conn.exec_driver_sql(f"ALTER TABLE {table} ADD COLUMN {name} {ddl}")
        conn.commit()


def get_session() -> Iterator[Session]:
    """FastAPI dependency."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@contextmanager
def session_scope() -> Iterator[Session]:
    """For use outside request handlers (sync jobs, CLI)."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
