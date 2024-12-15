import pandas as pd
import numpy as np
import calendar
import pandas as pd
import requests
from geopy.distance import geodesic

def get_days_in_month(year, month):
    _, num_days = calendar.monthrange(year, month)
    return num_days

def get_day_in_year(year, month, day):
    day_in_year = 0

    for m in range(1, month):
        day_in_year += get_days_in_month(year, m)

    day_in_year += day - 1

    return day_in_year

def add_hour_features(df):
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    
    return df
def add_day_in_year_features(df):
    # Convertir la variable 'day_in_year' a variables cícliches
    df['day_in_year_sin'] = np.sin(2 * np.pi * df['day_in_year'] / 365)
    df['day_in_year_cos'] = np.cos(2 * np.pi * df['day_in_year'] / 365)
    
    return df

def add_time_features(df):
    df = add_hour_features(df)
    
    df = add_day_in_year_features(df)
    
    return df

def acostar_a_1(x, factor=0.1):
    return x + (1 - x) * factor

def was_it_raining(rainfall_df, lat, lon, date):
    filtered = rainfall_df[
        (rainfall_df["lat"] == lat) & 
        (rainfall_df["lon"] == lon) & 
        (rainfall_df["date"] == date.strftime("%Y-%m-%d")) & 
        (rainfall_df["hour"] == date.hour)
    ]
    return filtered["rain"].iloc[0] > 0 if not filtered.empty else False
    
def fetch_rainfall_data(lat, lon, start_date, end_date):
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    rain_data = []

    for date in dates:
        formatted_date = date.strftime("%Y-%m-%d")
        url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={formatted_date}&end_date={formatted_date}&hourly=rain"
        
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and "hourly" in data:
            for i, rain in enumerate(data["hourly"]["rain"]):
                hour = i
                day_of_year = date.timetuple().tm_yday
                rain_data.append({"date": formatted_date, "hour": hour, "lat": lat, "lon": lon, "rain": rain})
        else:
            print(f"No data for {formatted_date}")

    return pd.DataFrame(rain_data)

def create_rainfall_dataset(locations, start_date="2023-01-01", end_date="2023-12-31"):
    all_rain_data = []
    for lat, lon in locations:
        print(f"Fetching rain data for location: ({lat}, {lon})")
        rain_df = fetch_rainfall_data(lat, lon, start_date, end_date)
        all_rain_data.append(rain_df)
    
    return pd.concat(all_rain_data, ignore_index=True)

def filter_by_radius(data_transformed, center_lat, center_lon, radius_km, k):
    unique_coords = data_transformed[['lat', 'lon']].drop_duplicates()
    
    unique_coords['distance'] = unique_coords.apply(
        lambda row: geodesic((center_lat, center_lon), (row['lat'], row['lon'])).km, axis=1
    )
    
    within_radius = unique_coords[unique_coords['distance'] <= radius_km]
    
    top_k_coords = within_radius.nsmallest(k, 'distance')
    
    result_df = data_transformed.merge(top_k_coords[['lat', 'lon']], on=['lat', 'lon'])
    
    return result_df

import pandas as pd
import matplotlib.pyplot as plt

def plot_concentration_vs_time(df):
    df['date'] = pd.to_datetime(df['date'])

    plt.figure(figsize=(12, 6))
    plt.scatter(df['date'], df['concentration'], color='blue', s=10, label='Concentración de NO₂')

    plt.xlabel('Fecha y Hora')
    plt.ylabel('Concentración de NO₂ (µg/m³)')
    plt.title('Concentración de NO₂ a lo largo del tiempo')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
