import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
CLEANED_DIR = ROOT / "data" / "cleaned"
CLEANED_FILE = CLEANED_DIR / "earthquakes_cleaned.csv"

TIME_KEYS = ["timestamp", "time", "date", "Tarih", "tarih", "date_time"]
LAT_KEYS = ["latitude", "lat", "enlem"]
LON_KEYS = ["longitude", "lon", "boylam"]
DEPTH_KEYS = ["depth", "derinlik"]
MAG_KEYS = ["magnitude", "mag", "Ml", "Mw"]
REGION_KEYS = ["region", "location", "place", "lokasyon", "yer", "title"]


def ensure_cleaned_dir() -> None:
    CLEANED_DIR.mkdir(parents=True, exist_ok=True)


def _find_value(record: Dict[str, Any], keys: List[str]) -> Any:
    for key in keys:
        if key in record:
            return record[key]
    return None


def _normalize_timestamp(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        if value > 1e12:
            value = int(value / 1000)
        return datetime.utcfromtimestamp(int(value)).isoformat()
    return pd.to_datetime(value, errors="coerce", utc=True)


def _parse_record(record: Dict[str, Any], source: str) -> Dict[str, Any]:
    # Handle geojson coordinates
    coords = record.get("geojson", {}).get("coordinates", [])
    if len(coords) >= 2:
        lon, lat = coords[0], coords[1]
    else:
        lon, lat = None, None

    return {
        "timestamp": _normalize_timestamp(_find_value(record, TIME_KEYS)),
        "latitude": pd.to_numeric(lat or _find_value(record, LAT_KEYS), errors="coerce"),
        "longitude": pd.to_numeric(lon or _find_value(record, LON_KEYS), errors="coerce"),
        "depth": pd.to_numeric(_find_value(record, DEPTH_KEYS), errors="coerce"),
        "magnitude": pd.to_numeric(_find_value(record, MAG_KEYS), errors="coerce"),
        "region": str(_find_value(record, REGION_KEYS) or "").strip(),
        "source": source,
    }


def _unwrap_json(raw: Any) -> Iterable[Dict[str, Any]]:
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        if "features" in raw and isinstance(raw["features"], list):
            return [item.get("properties", item) for item in raw["features"]]
        for key in ["result", "data", "earthquakes", "deprem", "records", "items"]:
            if key in raw and isinstance(raw[key], list):
                return raw[key]
        return [raw]
    return []


def load_raw_file(path: Path) -> List[Dict[str, Any]]:
    raw_text = path.read_text(encoding="utf-8")
    raw = json.loads(raw_text)
    return list(_unwrap_json(raw))


def clean_all_raw_files() -> pd.DataFrame:
    ensure_cleaned_dir()
    frames = []
    for path in sorted(RAW_DIR.glob("*.json")):
        records = load_raw_file(path)
        if not records:
            continue
        parsed = [_parse_record(record, source=path.name) for record in records]
        frames.append(pd.DataFrame(parsed))

    if not frames:
        return pd.DataFrame(
            columns=["timestamp", "latitude", "longitude", "depth", "magnitude", "region", "source"]
        )

    df = pd.concat(frames, ignore_index=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    df = df.dropna(subset=["timestamp", "latitude", "longitude", "magnitude"])
    df = df.sort_values("timestamp")
    df.to_csv(CLEANED_FILE, index=False)
    return df


def main() -> None:
    df = clean_all_raw_files()
    print(f"Cleaned {len(df)} earthquake records and saved to {CLEANED_FILE}")


if __name__ == "__main__":
    main()
