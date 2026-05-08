# Earthquake Pipeline

Bu proje, Türkiye deprem verilerini periyodik olarak çekmek, ham ve temizlenmiş veri katmanları oluşturmak, SQL sorguları çalıştırmak ve Streamlit dashboard ile görselleştirmek için hazırlanmıştır.

## Quick start

1. Yeni bir sanal ortam oluşturun ve bağımlılıkları yükleyin:

```bash
cd /path/to/earthquake_pipeline
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Dashboard'ı başlatın:

```bash
streamlit run src/dashboard.py
```

Not: Projeyi klonladıktan sonra `.venv` klasörünü repoya eklemeyin; proje kökünde `.gitignore` dosyası halihazırda bu klasörü hariç tutar.

## Adımlar

1. Ortamı hazırla

```bash
python -m pip install -r requirements.txt
```

2. Ham veriyi çek

```bash
python src/fetch_data.py
```

3. Veriyi temizle

```bash
python src/transform.py
```

4. Temiz veriyi SQLite veritabanına yükle

```bash
python src/load.py
```

5. Dashboard çalıştır

```bash
streamlit run src/dashboard.py
```

## Dosya Açıklamaları

- `src/fetch_data.py`: Ham deprem verisini API'den çeker ve `data/raw/` altında kaydeder.
- `src/transform.py`: Ham JSON verisini okur, normalize eder ve `data/cleaned/` altına temizlenmiş CSV kaydeder.
- `src/load.py`: Temizlenmiş CSV'yi SQLite veritabanına yükler.
- `src/queries.sql`: Sorgulama için hazır SQL örnekleri içerir.
- `src/dashboard.py`: Streamlit ile temel görselleştirme sağlar.

## Notlar

- `data/raw/` klasörüne her `fetch_data.py` çağrısında yeni bir JSON dosyası eklenir.
- `fetch_data.py` içindeki `DATA_SOURCE_URL` alanını kendi veri kaynağına göre güncelleyebilirsiniz.
- `db/earthquakes.db` veritabanını `src/load.py` oluşturur.

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

