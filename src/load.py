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


def main() -> None:
    df = load_cleaned_data()
    write_to_sqlite(df)


if __name__ == "__main__":
    main()
