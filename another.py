import requests
import pandas as pd
from datetime import datetime

# Constants
API_KEY = '8d41c409cd23d12b1a4a75903dc66503'
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"
CITIES = [
    {"name": "Bagerhat", "lat": 22.6516, "lon": 89.7857},
    # Add more cities with lat and lon here
]

# Function to fetch 3-hour interval forecast for the next 5 days
def get_forecast_data(lat, lon):
    url = f"{BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data: {response.status_code}, {response.text}")
        return None

# Function to extract the 3-hour forecast data
def extract_forecast_data(city):
    forecast_data = get_forecast_data(city['lat'], city['lon'])
    if not forecast_data:
        return None
    
    data = []
    for forecast in forecast_data['list']:
        forecast_info = {
            'City': city['name'],
            'DateTime': pd.to_datetime(forecast['dt'], unit='s').strftime('%Y-%m-%d %H:%M:%S'),
            'Temp': forecast['main']['temp'],
            'MinTemp': forecast['main']['temp_min'],
            'MaxTemp': forecast['main']['temp_max'],
            'Humidity': forecast['main']['humidity'],
            'WindSpeed': forecast['wind']['speed'],
            'CloudCover': forecast['clouds']['all'],
            'Rainfall': forecast.get('rain', {}).get('3h', 0),  # Rainfall in the last 3 hours, if available
            'Weather': forecast['weather'][0]['description']
        }
        data.append(forecast_info)
    return data

# Collect forecast data for all cities
all_forecast_data = []
for city in CITIES:
    city_forecast = extract_forecast_data(city)
    if city_forecast:
        all_forecast_data.extend(city_forecast)

# Convert to DataFrame and save to CSV
df = pd.DataFrame(all_forecast_data)
df.to_csv('3_hour_forecast.csv', index=False)
print("3-hour forecast data has been successfully saved to '3_hour_forecast.csv'.")
