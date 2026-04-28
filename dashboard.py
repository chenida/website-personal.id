import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Bike Sharing Analytics", layout="wide")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("all_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# --- SIDEBAR ---
st.sidebar.header("Filter Data")
date_range = st.sidebar.date_input(
    "Rentang Waktu",
    value=[df['dteday'].min(), df['dteday'].max()],
    min_value=df['dteday'].min(),
    max_value=df['dteday'].max()
)

# Filter dataframe berdasarkan sidebar
main_df = df[(df['dteday'] >= pd.to_datetime(date_range[0])) & 
            (df['dteday'] <= pd.to_datetime(date_range[1]))]

# --- MAIN PAGE ---
st.title("🚲 Bike Sharing Interactive Dashboard")
st.markdown("Analisis tren penyewaan sepeda berdasarkan faktor waktu dan cuaca.")

# --- METRICS SECTION ---
col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = main_df['count_hourly'].sum()
    st.metric("Total Penyewaan", f"{total_rentals:,}")
with col2:
    avg_temp = main_df['temp'].mean()
    st.metric("Rata-rata Suhu (Normalised)", f"{avg_temp:.2f}")
with col3:
    avg_hum = main_df['humidity'].mean()
    st.metric("Rata-rata Kelembapan", f"{avg_hum:.2f}")

st.divider()

# --- VISUALIZATION 1: Tren Per Jam ---
st.subheader("📊 Tren Penyewaan Berdasarkan Jam")
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=main_df, x='hr', y='count_hourly', hue='workingday', ax=ax, marker='o')
ax.set_xlabel("Jam (0-23)")
ax.set_ylabel("Jumlah Penyewa")
ax.legend(title="Hari Kerja", labels=["Libur/Weekend", "Hari Kerja"])
st.pyplot(fig)

# --- VISUALIZATION 2: Cuaca & Pengguna ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("☁️ Pengaruh Kondisi Cuaca")
    # Weather labels: 1: Clear, 2: Mist, 3: Light Snow/Rain, 4: Heavy Rain
    weather_map = {1: "Cerah", 2: "Berawan", 3: "Hujan Ringan", 4: "Hujan Lebat"}
    main_df['weather_label'] = main_df['weather_condition'].map(weather_map)
    
    fig, ax = plt.subplots()
    sns.barplot(data=main_df, x='weather_label', y='count_hourly', palette="viridis", ax=ax)
    st.pyplot(fig)

with col_right:
    st.subheader("👥 Casual vs Registered")
    total_casual = main_df['casual_hour'].sum()
    total_registered = main_df['registered_hour'].sum()
    
    fig, ax = plt.subplots()
    ax.pie([total_casual, total_registered], labels=['Casual', 'Registered'], 
           autopct='%1.1f%%', colors=['#ff9999','#66b3ff'], startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

# --- VISUALIZATION 3: Suhu vs Jumlah Penyewa ---
st.subheader("🌡️ Korelasi Suhu terhadap Penyewaan")
fig, ax = plt.subplots(figsize=(10, 4))
sns.scatterplot(data=main_df, x='temp', y='count_hourly', alpha=0.1, color='orange')
ax.set_xlabel("Suhu (Normalisasi)")
ax.set_ylabel("Jumlah Penyewa")
st.pyplot(fig)

st.caption("Copyright © 2024 - Bike Analysis Dashboard")