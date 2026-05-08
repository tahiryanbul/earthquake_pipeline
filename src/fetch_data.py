import json
import ssl
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"

# Kandilli veya AFAD gibi bir API uç noktası belirtin.
# Geçerli JSON endpoint örneği:
#   https://api.orhanaydogdu.com.tr/deprem/
DATA_SOURCE_URL = "https://api.orhanaydogdu.com.tr/deprem/"
DATA_SOURCE_TYPE = "json"  # "json" veya "csv"


class TLSAdapter(HTTPAdapter):
    def __init__(self, ssl_context: ssl.SSLContext = None, **kwargs: Any) -> None:
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections: int, maxsize: int, block: bool = False, **pool_kwargs: Any) -> None:
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ssl_context,
            **pool_kwargs,
        )


def create_session() -> requests.Session:
    context = ssl.create_default_context()
    try:
        context.minimum_version = ssl.TLSVersion.TLSv1_2
    except AttributeError:
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1

    session = requests.Session()
    session.mount("https://", TLSAdapter(ssl_context=context))
    session.headers.update({
        "User-Agent": "EarthquakePipeline/1.0 (+https://github.com)"
    })
    return session


def ensure_raw_dir() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)


def remove_old_raw_files(keep_filename: str) -> None:
    for path in RAW_DIR.glob("earthquakes_*"):
        if path.name != keep_filename:
            try:
                path.unlink()
            except OSError:
                pass


def download_data(url: str, data_type: str) -> Any:
    session = create_session()
    response = session.get(url, timeout=15)
    response.raise_for_status()
    if data_type.lower() == "csv":
        return response.text
    return response.json()


def save_raw(data: Any, prefix: str = "earthquakes", data_type: str = "json") -> Path:
    extension = "csv" if data_type.lower() == "csv" else "json"
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    file_path = RAW_DIR / f"{prefix}_latest.{extension}"

    if data_type.lower() == "csv":
        with file_path.open("w", encoding="utf-8") as fh:
            fh.write(data)
    else:
        with file_path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)

    return file_path


def fetch_and_save() -> Path:
    ensure_raw_dir()
    payload = download_data(DATA_SOURCE_URL, DATA_SOURCE_TYPE)
    saved_path = save_raw(payload, data_type=DATA_SOURCE_TYPE)
    remove_old_raw_files(saved_path.name)
    return saved_path


def main() -> None:
    saved_path = fetch_and_save()
    print(f"Saved raw earthquake data to: {saved_path}")


if __name__ == "__main__":
    main()
