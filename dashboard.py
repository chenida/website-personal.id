import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Helper function untuk menyiapkan DataFrame pendukung
def create_daily_rent_df(df):
    # Mengelompokkan berdasarkan hari dan menjumlahkan total rental
    daily_rent_df = df.resample(rule='D', on='dteday').agg({
        "total_daily_count": "sum",
        "casual_day": "sum",
        "registered_day": "sum"
    })
    daily_rent_df = daily_rent_df.reset_index()
    return daily_rent_df

def create_by_weather_df(df):
    # Rata-rata rental berdasarkan kondisi cuaca
    weather_df = df.groupby("weather_condition").total_daily_count.mean().reset_index()
    weather_df.rename(columns={"total_daily_count": "avg_rentals"}, inplace=True)
    return weather_df

def create_by_hour_df(df):
    # Pola rental berdasarkan jam (menggunakan count_hourly)
    hour_df = df.groupby("hr").count_hourly.mean().reset_index()
    return hour_df

# Load dataset
all_df = pd.read_csv("all_data.csv")

# Pastikan kolom dteday bertipe datetime
all_df["dteday"] = pd.to_datetime(all_df["dteday"])
all_df.sort_values(by="dteday", inplace=True)

# --- SIDEBAR ---
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Filter Rentang Waktu
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter Data Utama
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

# Menyiapkan helper dataframes
daily_rent_df = create_daily_rent_df(main_df)
weather_df = create_by_weather_df(main_df)
hour_df = create_by_hour_df(main_df)

# --- MAIN PAGE ---
st.header('Bike Sharing Dashboard 🚲')

# 1. Daily Rentals Metrics
st.subheader('Daily Rentals Overview')
col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = daily_rent_df.total_daily_count.sum()
    st.metric("Total Rentals", value=total_rentals)

with col2:
    total_casual = daily_rent_df.casual_day.sum()
    st.metric("Casual Users", value=total_casual)

with col3:
    total_registered = daily_rent_df.registered_day.sum()
    st.metric("Registered Users", value=total_registered)

# Plot Daily Rentals
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rent_df["dteday"],
    daily_rent_df["total_daily_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.set_title("Trend of Daily Bike Rentals", fontsize=25)
ax.tick_params(axis='both', labelsize=15)
st.pyplot(fig)

# 2. Weather Condition Impact
st.subheader("Rentals by Weather Condition")
fig, ax = plt.subplots(figsize=(12, 6))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="weather_condition", 
    y="avg_rentals", 
    data=weather_df, 
    palette=colors, 
    ax=ax
)
ax.set_title("Average Rentals based on Weather Condition", fontsize=20)
ax.set_xlabel("Weather Condition (1: Clear, 2: Mist, 3: Light Snow/Rain)", fontsize=15)
ax.set_ylabel("Average Count", fontsize=15)
st.pyplot(fig)

# 3. Hourly Patterns
st.subheader("Hourly Rental Patterns")
fig, ax = plt.subplots(figsize=(12, 6))

sns.lineplot(
    x="hr", 
    y="count_hourly", 
    data=hour_df, 
    marker='o', 
    color="#FF9800",
    ax=ax
)
ax.set_title("Average Bike Rentals per Hour", fontsize=20)
ax.set_xticks(range(0, 24))
ax.set_xlabel("Hour of the Day", fontsize=15)
ax.set_ylabel("Average Count", fontsize=15)
ax.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig)

st.caption('Copyright (c) BikeShare Analytics 2026')