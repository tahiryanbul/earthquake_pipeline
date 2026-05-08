# Earthquake Pipeline

This project fetches earthquake data for Türkiye on a recurring basis, produces raw and cleaned data layers, runs SQL queries, and provides a Streamlit dashboard for visualization.

## Quick start

1. Create a virtual environment and install dependencies:

```bash
cd /path/to/earthquake_pipeline
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Start the dashboard:

```bash
streamlit run src/dashboard.py
```

Note: Do not add `.venv` to the repository. The repository already includes a `.gitignore` entry to exclude it.

## Steps

1. Prepare environment

```bash
python -m pip install -r requirements.txt
```

2. Fetch raw data

```bash
python src/fetch_data.py
```

3. Clean and normalize data

```bash
python src/transform.py
```

4. Load cleaned data into SQLite

```bash
python src/load.py
```

### Optional: Load into PostgreSQL

`src/load.py` can write to a PostgreSQL database instead of SQLite. To enable Postgres writing set `USE_POSTGRES=1` and provide connection details via environment variables. Example:

```bash
export POSTGRES_USER=youruser
export POSTGRES_PASSWORD=yourpass
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=earthquakes
export USE_POSTGRES=1
python src/load.py
```

You can also place these variables in a `.env` file and load them with `python-dotenv` (package added to `requirements.txt`).

5. Run the dashboard

```bash
streamlit run src/dashboard.py
```

## File overview

- `src/fetch_data.py`: Downloads raw earthquake data from an API into `data/raw/`.
- `src/transform.py`: Reads raw JSON, normalizes records, and writes a cleaned CSV to `data/cleaned/`.
- `src/load.py`: Loads the cleaned CSV into an SQLite database.
- `src/queries.sql`: Example SQL queries for analysis.
- `src/dashboard.py`: Streamlit dashboard for visualizing the data.

## Notes

- Each run of `fetch_data.py` will add a JSON file to `data/raw/`.
- Update `DATA_SOURCE_URL` in `src/fetch_data.py` if you want to point to a different API source.
- The SQLite database `db/earthquakes.db` is created by `src/load.py`.

## Compatibility & reproducibility

- Recommended Python: 3.10 or newer. A virtual environment is required to avoid system package conflicts.
- Use the provided `setup.sh` script to create a `.venv` and install pinned dependencies.

```bash
cd /path/to/earthquake_pipeline
./setup.sh
source .venv/bin/activate
streamlit run src/dashboard.py
```

Notes:
- `requirements.txt` contains pinned package versions to provide reproducible installs across machines.
- Do not commit `.venv`, `data/`, or `db/` to the repository (they are added to `.gitignore`).
- The pipeline fetches data from an external API (`DATA_SOURCE_URL` in `src/fetch_data.py`); make sure network access is available or replace the data source with a local file for offline tests.

### Offline testing with sample data

A small sample dataset is included at `data/sample/earthquakes_sample.json` for offline testing. To use it:

```bash
# copy sample into the raw data folder where the pipeline expects raw files
mkdir -p data/raw
cp data/sample/earthquakes_sample.json data/raw/earthquakes_sample.json

# run the transform and load steps
python src/transform.py
python src/load.py

# then run the dashboard
streamlit run src/dashboard.py
```


### Windows notes

To set up and run the project on Windows, use PowerShell or CMD and the appropriate activate command:

- PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run src/dashboard.py
```

- Command Prompt (cmd.exe):

```cmd
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run src/dashboard.py
```

If a package requires compilation on Windows, install the recommended build tools (e.g., Visual Studio Build Tools) or use the Windows Subsystem for Linux (WSL) for a Linux-like environment.

