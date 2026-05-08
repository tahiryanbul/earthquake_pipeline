from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
CLEANED_FILE = ROOT / "data" / "cleaned" / "earthquakes_cleaned.csv"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(CLEANED_FILE, parse_dates=["timestamp"])
    df = df.sort_values("timestamp")
    return df


def main() -> None:
    st.set_page_config(page_title="Türkiye Earthquake Dashboard", layout="wide")
    st.title("Türkiye Earthquake Data Pipeline")

    df = load_data()
    st.write("### Temizlenmiş Deprem Verisi")
    st.write(df.head(20))

    if df.empty:
        st.warning("Henüz temizlenmiş veri yok. önce fetch_data.py ve transform.py çalıştırın.")
        return

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("Toplam Deprem", len(df))
    col2.metric("Son Kayıt", str(df["timestamp"].max().date()) if not df.empty else "N/A")
    col3.metric("Benzersiz Bölge", df["region"].nunique())

    st.markdown("---")
    st.subheader("En Aktif Bölgeler")
    top_regions = df["region"].value_counts().head(15).reset_index()
    top_regions.columns = ["Bölge", "Deprem Sayısı"]
    st.bar_chart(top_regions.rename(columns={"Bölge": "index"}).set_index("index"))

    st.subheader("Saatlik Deprem Yoğunluğu")
    hourly = (
        df.set_index("timestamp")
        .resample("1h")
        .size()
        .rename("count")
        .reset_index()
    )
    hourly["hour"] = hourly["timestamp"].dt.strftime("%Y-%m-%d %H:00")
    st.line_chart(hourly.set_index("hour")["count"])

    st.subheader("Magnitude Dağılımı")
    bins = [0, 2, 4, 5, 6, 10]
    labels = ["<2", "2-4", "4-5", "5-6", "6+"]
    df["mag_bin"] = pd.cut(df["magnitude"], bins=bins, labels=labels, right=False)
    mag_counts = df["mag_bin"].value_counts().sort_index().rename_axis("Magnitude").reset_index(name="count")
    st.bar_chart(mag_counts.set_index("Magnitude"))

    st.subheader("Deprem Noktaları Haritası")
    st.map(df.rename(columns={"latitude": "lat", "longitude": "lon"})[["lat", "lon"]].dropna())


if __name__ == "__main__":
    main()
