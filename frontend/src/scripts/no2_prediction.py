import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import calendar
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from geopy.distance import geodesic
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
import requests
from datetime import datetime
import geopandas as gpd

from populationOffset import popOffset
import no2_utils as no2_utils

data_transformed = pd.read_csv("../Data/Data_Transformed.csv")
data_rainFall = pd.read_csv("../Data/Rainfall_Info.csv")

def predict_no2_concentration(lat, lon):
    print(f"Predint la concentració de NO2 per latitud: {lat}, longitud: {lon}")

    radius = 3
    data_near = no2_utils.filter_by_radius(data_transformed, lat, lon, radius,6)

    
    print(f"Creant el model de predicció per al temps amb les dades de les estacions pròximes: ")

    X = data_near[['hour_sin', 'hour_cos', 'day_in_year_sin', 'day_in_year_cos']]
    y = data_near['concentration']
    
    y_mean = y.mean()
    y_normalized = (y - y_mean) / y_mean
    
    poly = PolynomialFeatures(degree=10, include_bias=True)
    model = make_pipeline(poly, LinearRegression())
    
    model.fit(X, y_normalized)
    model = (lat, lon, model, y_mean)

    dates = pd.date_range(start="2023-01-01 00:00", end="2023-12-31 23:00", freq="H")

    data = []
    id_counter = 1

    print(f"Processant prediccions...")

    model_info = model
    if model_info is None:
        raise ValueError(f"No s'ha trobat un model per predir el temps en ({lat}, {lon})")
    
    model, y_mean = model_info[2], model_info[3]
    
    avg_concentration = data_near["concentration"].mean()
    
    for date in dates:
        hour = date.hour
        day_of_year = date.timetuple().tm_yday
        
        hour_sin = np.sin(2 * np.pi * hour / 24)
        hour_cos = np.cos(2 * np.pi * hour / 24)
        day_sin = np.sin(2 * np.pi * day_of_year / 365)
        day_cos = np.cos(2 * np.pi * day_of_year / 365)
        
        X_single = pd.DataFrame({
            'hour_sin': [hour_sin],
            'hour_cos': [hour_cos],
            'day_in_year_sin': [day_sin],
            'day_in_year_cos': [day_cos],
        })
        
        time_coeficient = model.predict(X_single)[0]

        rain_coeficient = 1
        if no2_utils.was_it_raining(data_rainFall, lat, lon, date):
            rain_coeficient = 0.95
        
        data.append({
            "id": id_counter,
            "date": date.strftime("%Y-%m-%d %H:%M"),
            "lat": lat, 
            "lon": lon, 
            "concentration": (avg_concentration + (time_coeficient * avg_concentration))*rain_coeficient
        })
        id_counter += 1

    print("S'ha calculat correctament la predicció")
    output = pd.DataFrame(data)

    output_csv_path = "../Output/output_kaggle.csv"
    output.to_csv(output_csv_path, index=False)

    return output
