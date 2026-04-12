import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set gaya visualisasi
sns.set(style='dark')

# --- Helper Functions untuk Menyiapkan Dataframe ---

def create_daily_rentals_df(df):
    # Menggunakan max karena cnt_day bernilai sama untuk setiap jam di hari yang sama
    daily_rentals_df = df.resample(rule='D', on='dteday').agg({
        "cnt_day": "max",
        "casual_day": "max",
        "registered_day": "max"
    })
    daily_rentals_df = daily_rentals_df.reset_index()
    daily_rentals_df.rename(columns={
        "cnt_day": "total_count",
        "casual_day": "casual",
        "registered_day": "registered"
    }, inplace=True)
    
    return daily_rentals_df

def create_season_rentals_df(df):
    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    df_copy = df.copy()
    df_copy['season_label'] = df_copy['season_day'].map(season_mapping)
    season_rentals_df = df_copy.groupby("season_label").cnt_day.mean().sort_values(ascending=False).reset_index()
    return season_rentals_df

def create_byweather_df(df):
    weather_mapping = {1: "Clear", 2: "Mist", 3: "Light Snow", 4: "Heavy Rain"}
    df_copy = df.copy()
    df_copy['weather_label'] = df_copy['weathersit_day'].map(weather_mapping)
    byweather_df = df_copy.groupby(by="weather_label").cnt_day.mean().reset_index()
    byweather_df.rename(columns={"cnt_day": "avg_rentals"}, inplace=True)
    return byweather_df

def create_byworkingday_df(df):
    workday_mapping = {0: "Holiday/Weekend", 1: "Working Day"}
    df_copy = df.copy()
    df_copy['workday_label'] = df_copy['workingday_day'].map(workday_mapping)
    byworkday_df = df_copy.groupby(by="workday_label").cnt_day.mean().reset_index()
    byworkday_df.rename(columns={"cnt_day": "avg_rentals"}, inplace=True)
    return byworkday_df

def create_hourly_df(df):
    hourly_df = df.groupby(by="hr").cnt_hour.mean().reset_index()
    return hourly_df

# --- Load Data ---
# Memastikan membaca file 'all_data.csv' sesuai dengan data yang tersedia
all_df = pd.read_csv("all_data.csv")

# Konversi kolom dteday menjadi datetime
all_df["dteday"] = pd.to_datetime(all_df["dteday"])
all_df.sort_values(by="dteday", inplace=True)

# --- Filter Sidebar ---
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Logo Placeholder
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Input rentang waktu
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Memfilter dataframe berdasarkan input user
main_df = all_df[(all_df["dteday"] >= pd.to_datetime(start_date)) & 
                 (all_df["dteday"] <= pd.to_datetime(end_date))]

# Menyiapkan dataframe turunan untuk visualisasi
daily_rentals_df = create_daily_rentals_df(main_df)
season_rentals_df = create_season_rentals_df(main_df)
byweather_df = create_byweather_df(main_df)
byworkday_df = create_byworkingday_df(main_df)
hourly_df = create_hourly_df(main_df)

# --- Layout Dashboard ---

st.header('Bike Sharing Analysis Dashboard :bike:')
st.subheader('Daily Rentals')

col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = daily_rentals_df.total_count.sum()
    st.metric("Total Rentals", value=f"{total_rentals:,}")

with col2:
    total_casual = daily_rentals_df.casual.sum()
    st.metric("Total Casual", value=f"{total_casual:,}")

with col3:
    total_registered = daily_rentals_df.registered.sum()
    st.metric("Total Registered", value=f"{total_registered:,}")

# Visualisasi 1: Tren Penyewaan Harian
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rentals_df["dteday"],
    daily_rentals_df["total_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.set_title("Daily Total Bike Rentals Trend", fontsize=25)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Visualisasi 2: Performa Berdasarkan Musim
st.subheader("Rental Performance by Season")
fig, ax = plt.subplots(figsize=(16, 8))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x="cnt_day", 
    y="season_label", 
    data=season_rentals_df, 
    palette=colors, 
    ax=ax
)
ax.set_title("Average Rentals by Season", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel("Average Number of Rentals", fontsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Visualisasi 3: Dampak Cuaca dan Hari Kerja
st.subheader("Weather and Day Type Impact")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        y="avg_rentals", 
        x="weather_label",
        data=byweather_df.sort_values(by="avg_rentals", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Avg Rentals by Weather", loc="center", fontsize=18)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        y="avg_rentals", 
        x="workday_label",
        data=byworkday_df.sort_values(by="avg_rentals", ascending=False),
        palette=["#D3D3D3", "#90CAF9"],
        ax=ax
    )
    ax.set_title("Avg Rentals: Working Day vs Weekend", loc="center", fontsize=18)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    st.pyplot(fig)

# Visualisasi 4: Pola Per Jam
st.subheader("Hourly Rental Patterns")
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(
    x="hr", 
    y="cnt_hour", 
    data=hourly_df, 
    marker='o', 
    color="#90CAF9", 
    ax=ax
)
ax.set_title("Average Bike Rentals by Hour", fontsize=25)
ax.set_xlabel("Hour (0-23)", fontsize=20)
ax.set_ylabel("Average Rentals", fontsize=20)
ax.set_xticks(range(0, 24))
ax.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig)

st.caption('Copyright © Dicoding 2024 - Bike Sharing Analysis Dashboard')