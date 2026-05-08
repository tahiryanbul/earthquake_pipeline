import os
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB_DIR = ROOT / "db"
DB_FILE = DB_DIR / "earthquakes.db"
CLEANED_FILE = ROOT / "data" / "cleaned" / "earthquakes_cleaned.csv"
TABLE_NAME = "earthquakes"


def ensure_db_dir() -> None:
    DB_DIR.mkdir(parents=True, exist_ok=True)


def create_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            timestamp TEXT,
            latitude REAL,
            longitude REAL,
            depth REAL,
            magnitude REAL,
            region TEXT,
            source TEXT
        )
        """
    )
    conn.commit()


def load_cleaned_data() -> pd.DataFrame:
    return pd.read_csv(CLEANED_FILE, parse_dates=["timestamp"])


def write_to_sqlite(df: pd.DataFrame) -> None:
    ensure_db_dir()
    with sqlite3.connect(DB_FILE) as conn:
        create_table(conn)
        df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
    print(f"Loaded {len(df)} rows into SQLite database: {DB_FILE}")


def get_postgres_engine():
    try:
        from sqlalchemy import create_engine
    except Exception as e:
        raise RuntimeError(f"SQLAlchemy is required for Postgres support: {e}")

    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "earthquakes")
    return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")


def write_to_postgres(df: pd.DataFrame) -> None:
    engine = get_postgres_engine()
    # Use SQLAlchemy engine and pandas to_sql. Requires psycopg2 and sqlalchemy in requirements.
    with engine.begin() as conn:
        df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False, method="multi", chunksize=1000)
    print(f"Loaded {len(df)} rows into Postgres database: {engine.url}")


def main() -> None:
    df = load_cleaned_data()
    use_postgres = os.getenv("USE_POSTGRES", "0").lower() in ("1", "true", "yes")
    if use_postgres:
        write_to_postgres(df)
    else:
        write_to_sqlite(df)


if __name__ == "__main__":
    main()
