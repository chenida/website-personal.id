import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page title
st.set_page_config(page_title="Bike Sharing Analysis Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("all_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

st.title("📊 Bike Sharing Data Analysis Dashboard")
st.markdown("Dashboard ini menyajikan analisis penyewaan sepeda berdasarkan tren waktu dan suhu (2011-2012).")

# --- Bagian 1: Rata-rata Penyewaan per Jam ---
st.header("1. Rata-rata Penyewaan Sepeda per Jam")

# Menghitung rata-rata penyewaan per jam
hourly_rentals = df.groupby("hr")["count_hourly"].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 5))
sns.barplot(x="hr", y="count_hourly", data=hourly_rentals, palette="Blues_d", ax=ax)
ax.set_xlabel("Jam (0-23)")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_title("Distribusi Rata-rata Penyewaan Sepeda Berdasarkan Jam")
st.pyplot(fig)

# Menampilkan insight singkat
high_hour = hourly_rentals.loc[hourly_rentals['count_hourly'].idxmax(), 'hr']
low_hour = hourly_rentals.loc[hourly_rentals['count_hourly'].idxmin(), 'hr']
st.write(f"**Insight:** Rata-rata penyewaan tertinggi terjadi pada jam **{high_hour}:00**, sedangkan terendah pada jam **{low_hour}:00**.")

# --- Bagian 2: Tren Suhu per Jam dan Hari ---
st.header("2. Tren Rata-rata Suhu (Temperatur)")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Tren Suhu per Jam")
    hourly_temp = df.groupby("hr")["temp"].mean().reset_index()
    fig2, ax2 = plt.subplots()
    sns.lineplot(x="hr", y="temp", data=hourly_temp, marker='o', color='orange', ax=ax2)
    ax2.set_xlabel("Jam")
    ax2.set_ylabel("Rata-rata Suhu (Normalized)")
    st.pyplot(fig2)

with col2:
    st.subheader("Tren Suhu per Hari (Weekday)")
    # Menggunakan weekday (0=Minggu/Senin tergantung dataset, 6=Sabtu)
    daily_temp = df.groupby("weekday")["temp_day"].mean().reset_index()
    fig3, ax3 = plt.subplots()
    sns.lineplot(x="weekday", y="temp_day", data=daily_temp, marker='o', color='red', ax=ax3)
    ax3.set_xlabel("Hari (0-6)")
    ax3.set_ylabel("Rata-rata Suhu Harian")
    st.pyplot(fig3)

st.info("Catatan: Kolom 'temp' dan 'temp_day' merupakan nilai suhu yang telah dinormalisasi.")